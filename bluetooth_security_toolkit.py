#!/usr/bin/env python3

import sys
import time
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import bluetooth
from scapy.all import *
from bluepy.btle import Scanner, DefaultDelegate
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

class BluetoothSecurityScanner:
    def __init__(self, scan_duration: int = 10):
        self.scan_duration = scan_duration
        self.logger = self._setup_logging()
        self.devices = {}
        self.ble_devices = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Configure logging with colored output and file storage."""
        logger = logging.getLogger('BluetoothSecurity')
        logger.setLevel(logging.INFO)
        
        # Console handler with colored output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            f'{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - '
            f'{Fore.GREEN}%(levelname)s{Style.RESET_ALL} - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # File handler for detailed logging
        file_handler = logging.FileHandler(
            f'bluetooth_scan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def discover_classic_devices(self):
        """Scan for classic Bluetooth devices."""
        self.logger.info(f"{Fore.BLUE}[*] Scanning for Classic Bluetooth devices...{Style.RESET_ALL}")
        try:
            nearby_devices = bluetooth.discover_devices(
                duration=self.scan_duration,
                lookup_names=True,
                lookup_class=True
            )
            
            for addr, name, device_class in nearby_devices:
                self.devices[addr] = {
                    'name': name,
                    'class': device_class,
                    'type': 'Classic',
                    'services': self.enumerate_services(addr)
                }
                self.logger.info(
                    f"{Fore.GREEN}[+] Found Classic Device:{Style.RESET_ALL} "
                    f"{name} ({addr}) - Class: {device_class}"
                )
        except Exception as e:
            self.logger.error(f"{Fore.RED}[-] Error scanning Classic Bluetooth: {e}{Style.RESET_ALL}")

    def enumerate_services(self, addr: str) -> List[Dict]:
        """Enumerate services for a classic Bluetooth device."""
        services = []
        try:
            for service_matches in bluetooth.find_service(address=addr):
                services.append({
                    'name': service_matches['name'],
                    'protocol': service_matches['protocol'],
                    'port': service_matches['port'],
                    'service-classes': service_matches['service-classes'],
                    'profiles': service_matches['profiles'],
                    'service-id': service_matches['service-id']
                })
        except Exception as e:
            self.logger.error(f"{Fore.RED}[-] Error enumerating services for {addr}: {e}{Style.RESET_ALL}")
        return services

class BLEDelegate(DefaultDelegate):
    def __init__(self, logger):
        DefaultDelegate.__init__(self)
        self.logger = logger

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            self.logger.debug(f"Discovered new BLE device: {dev.addr}")
        elif isNewData:
            self.logger.debug(f"Received new data from {dev.addr}")

class BluetoothSecurityAssessment:
    def __init__(self):
        self.scanner = BluetoothSecurityScanner()
        
    def run_assessment(self):
        """Run the complete security assessment workflow."""
        self.scanner.logger.info(f"{Fore.YELLOW}[*] Starting Bluetooth Security Assessment{Style.RESET_ALL}")
        
        # Device Discovery Phase
        self.scanner.discover_classic_devices()
        self.scan_ble_devices()
        
        # Analysis Phase
        self.analyze_security_posture()
        
        # Report Generation
        self.generate_report()

    def scan_ble_devices(self):
        """Scan for BLE devices using bluepy."""
        self.scanner.logger.info(f"{Fore.BLUE}[*] Scanning for BLE devices...{Style.RESET_ALL}")
        try:
            scanner = Scanner().withDelegate(BLEDelegate(self.scanner.logger))
            devices = scanner.scan(self.scanner.scan_duration)
            
            for dev in devices:
                self.scanner.ble_devices[dev.addr] = {
                    'name': dev.getValueText(9) or "Unknown",
                    'rssi': dev.rssi,
                    'connectable': dev.connectable,
                    'adv_data': {
                        'manufacturer_data': dev.getValueText(255),
                        'complete_name': dev.getValueText(9),
                        'short_name': dev.getValueText(8),
                    }
                }
                self.scanner.logger.info(
                    f"{Fore.GREEN}[+] Found BLE Device:{Style.RESET_ALL} "
                    f"{dev.addr} (RSSI: {dev.rssi}dB)"
                )
        except Exception as e:
            self.scanner.logger.error(f"{Fore.RED}[-] Error scanning BLE devices: {e}{Style.RESET_ALL}")

    def analyze_security_posture(self):
        """Analyze the security posture of discovered devices."""
        self.scanner.logger.info(f"{Fore.YELLOW}[*] Analyzing device security posture...{Style.RESET_ALL}")
        
        for addr, device in self.scanner.devices.items():
            self._analyze_classic_device(addr, device)
            
        for addr, device in self.scanner.ble_devices.items():
            self._analyze_ble_device(addr, device)

    def _analyze_classic_device(self, addr: str, device: Dict):
        """Analyze security of classic Bluetooth device."""
        vulnerabilities = []
        
        # Check for common vulnerabilities
        if device['name'] and device['name'].lower() in ['hc-05', 'hc-06']:
            vulnerabilities.append("Default configuration detected - possible weak PIN")
        
        if device['services']:
            for service in device['services']:
                if service['protocol'] == 'RFCOMM':
                    vulnerabilities.append("RFCOMM service exposed - potential attack surface")

        if vulnerabilities:
            self.scanner.logger.warning(
                f"{Fore.YELLOW}[!] Vulnerabilities found for {addr}:{Style.RESET_ALL}\n" +
                "\n".join(f"  - {v}" for v in vulnerabilities)
            )

    def _analyze_ble_device(self, addr: str, device: Dict):
        """Analyze security of BLE device."""
        vulnerabilities = []
        
        if device['connectable']:
            vulnerabilities.append("Device is connectable - potential MITM attack vector")
        
        if device['rssi'] > -35:
            vulnerabilities.append("Very strong signal strength - possible proximity attack risk")

        if vulnerabilities:
            self.scanner.logger.warning(
                f"{Fore.YELLOW}[!] Vulnerabilities found for {addr}:{Style.RESET_ALL}\n" +
                "\n".join(f"  - {v}" for v in vulnerabilities)
            )

    def generate_report(self):
        """Generate a comprehensive security assessment report."""
        report_filename = f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        with open(report_filename, 'w') as f:
            f.write("Bluetooth Security Assessment Report\n")
            f.write("=" * 40 + "\n\n")
            
            f.write("1. Classic Bluetooth Devices\n")
            f.write("-" * 30 + "\n")
            for addr, device in self.scanner.devices.items():
                f.write(f"Device: {addr}\n")
                f.write(f"Name: {device['name']}\n")
                f.write(f"Class: {device['class']}\n")
                f.write("Services:\n")
                for service in device['services']:
                    f.write(f"  - {service['name']}\n")
                f.write("\n")
            
            f.write("\n2. BLE Devices\n")
            f.write("-" * 30 + "\n")
            for addr, device in self.scanner.ble_devices.items():
                f.write(f"Device: {addr}\n")
                f.write(f"Name: {device['name']}\n")
                f.write(f"RSSI: {device['rssi']}\n")
                f.write(f"Connectable: {device['connectable']}\n")
                f.write("\n")

def main():
    parser = argparse.ArgumentParser(description='Bluetooth Security Assessment Tool')
    parser.add_argument('--duration', type=int, default=10,
                      help='Scan duration in seconds (default: 10)')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Enable verbose output')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger('BluetoothSecurity').setLevel(logging.DEBUG)

    assessment = BluetoothSecurityAssessment()
    assessment.run_assessment()

if __name__ == '__main__':
    main() 