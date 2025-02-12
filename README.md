# Bluetooth Security Assessment Toolkit

A powerful and comprehensive toolkit for assessing Bluetooth security, performing penetration testing, and analyzing vulnerabilities in both Classic Bluetooth and BLE (Bluetooth Low Energy) devices.

## ⚠️ Important Notice

This tool is for **EDUCATIONAL AND RESEARCH PURPOSES ONLY**. Only use it on devices you own or have explicit permission to test. Unauthorized Bluetooth hacking is illegal and unethical.

## 🔑 Key Features

### 1. Device Discovery & Scanning
- Detects both Classic Bluetooth and BLE devices
- Extracts device information:
  - MAC addresses
  - Device names
  - Signal strength (RSSI)
  - Service UUIDs
  - Manufacturer data

### 2. Vulnerability Assessment
- Tests for common security weaknesses:
  - Just Works pairing vulnerability
  - KNOB attack susceptibility
  - Weak encryption configurations
  - Default credentials
- Analyzes device security posture
- Identifies potential attack vectors

### 3. Attack Capabilities
- Man-in-the-Middle (MITM) attacks
- Device spoofing
- Signal jamming
- Pairing request flooding
- Encryption downgrade attempts

### 4. Traffic Analysis
- Captures Bluetooth packets
- Monitors device communications
- Analyzes connection parameters
- Logs all findings for further analysis

## 🛠️ Requirements

### System Requirements
- Python 3.7 or higher
- Linux-based operating system (tested on Ubuntu/Debian)
- Root/sudo privileges
- Compatible Bluetooth adapter

### Required Tools
- Bettercap (for MITM attacks)
- btlejack (for jamming capabilities)
- Ubertooth One (optional, for advanced sniffing)

### Python Dependencies
```
pybluez>=0.23
scapy>=2.4.5
bluepy>=1.3.0
colorama>=0.4.6
python-dateutil>=2.8.2
btlejack>=2.0.0
pyubertooth>=0.2
dbus-python>=1.2.18
pygobject>=3.42.0
pycrypto>=2.6.1
```

## 📥 Installation

1. Install system dependencies:
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip python3-dev bluetooth libbluetooth-dev
sudo apt-get install bettercap btlejack ubertooth

# For Fedora/RHEL
sudo dnf install python3-devel bluetooth bluez-libs-devel
sudo dnf install bettercap btlejack ubertooth
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/bluetooth-security-toolkit.git
cd bluetooth-security-toolkit
```

3. Set up Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Scanning
```bash
sudo python bluetooth_security_toolkit.py
```

### Extended Scan with Verbose Output
```bash
sudo python bluetooth_security_toolkit.py --duration 30 --verbose
```

### Enable Attack Mode
```bash
sudo python bluetooth_security_toolkit.py --attack --duration 30
```

### Capture Bluetooth Traffic
```bash
sudo python bluetooth_security_toolkit.py --capture --duration 30
```

### Command Line Options
- `--duration`: Set scan duration in seconds (default: 10)
- `--verbose`: Enable detailed logging output
- `--attack`: Enable active attack capabilities
- `--capture`: Enable packet capture

## 📊 Output Files

The toolkit generates several output files:

1. **Scan Logs** (`bluetooth_scan_[timestamp].log`)
   - Detailed technical scan information
   - Device discovery results
   - Error messages and warnings

2. **Security Reports** (`security_report_[timestamp].txt`)
   - Comprehensive vulnerability assessment
   - Attack results (if attack mode enabled)
   - Security recommendations

3. **Packet Captures** (`bluetooth_capture_[timestamp].pcap`)
   - Raw Bluetooth traffic
   - Can be analyzed with Wireshark

## 🛡️ Security Considerations

1. **Legal Compliance**
   - Only test devices you own or have permission to test
   - Follow local laws and regulations
   - Respect privacy and data protection laws

2. **System Security**
   - Run with root privileges carefully
   - Monitor system resources during attacks
   - Be cautious with captured sensitive data

3. **Attack Impact**
   - Active attacks can disrupt legitimate devices
   - Some attacks may crash or damage vulnerable devices
   - Always have a plan to restore normal operation

## 🐛 Troubleshooting

Common issues and solutions:

1. **Permission Denied**
   ```bash
   sudo chmod +x bluetooth_security_toolkit.py
   ```

2. **Bluetooth Adapter Not Found**
   ```bash
   sudo hciconfig hci0 up
   ```

3. **Dependencies Issues**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## ⚠️ Disclaimer

This tool is for educational and security research purposes only. The authors are not responsible for any misuse, damage, or legal consequences caused by this tool. Users are responsible for complying with all applicable laws and regulations. The active attack capabilities should only be used in controlled testing environments with explicit permission. 