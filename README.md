# Bluetooth Security Assessment Toolkit

A comprehensive Bluetooth security assessment tool that performs device discovery, vulnerability scanning, security analysis, and active attacks against both Classic Bluetooth and BLE devices.

## Features

- Device Discovery & Enumeration
  - Scans for both Classic Bluetooth and BLE devices
  - Extracts device metadata (MAC addresses, names, signal strength)
  - Classifies devices based on type and manufacturer

- Active & Passive Reconnaissance
  - Intercepts BLE advertising packets
  - Enumerates available services and UUIDs
  - Monitors connection parameters
  - Captures and analyzes Bluetooth traffic

- Security Analysis
  - Tests for common vulnerabilities
  - Detects weak configurations
  - Identifies potential attack vectors
  - Analyzes encryption strength
  - Tests for Just Works pairing vulnerability
  - Checks for KNOB attack susceptibility

- Active Attack Capabilities
  - Man-in-the-Middle (MITM) attacks using Bettercap
  - Device spoofing and identity manipulation
  - Bluetooth signal jamming using btlejack
  - Pairing request flooding (DoS)
  - Forced encryption downgrade

- Detailed Reporting
  - Generates comprehensive security reports
  - Provides actionable remediation advice
  - Logs all findings with timestamps
  - Captures Bluetooth traffic for analysis

## Prerequisites

- Python 3.7+
- Linux-based system (some features require root privileges)
- Bluetooth adapter supporting both Classic and BLE
- Bettercap for MITM attacks
- btlejack for jamming capabilities
- Ubertooth One (optional, for advanced sniffing)

### System Dependencies

For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev bluetooth libbluetooth-dev
sudo apt-get install bettercap btlejack ubertooth
```

For Fedora/RHEL:
```bash
sudo dnf install python3-devel bluetooth bluez-libs-devel
sudo dnf install bettercap btlejack ubertooth
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bluetooth-security-toolkit.git
cd bluetooth-security-toolkit
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic scan:
```bash
sudo python bluetooth_security_toolkit.py
```

Extended scan with verbose output:
```bash
sudo python bluetooth_security_toolkit.py --duration 30 --verbose
```

Enable active attacks:
```bash
sudo python bluetooth_security_toolkit.py --attack --duration 30
```

Enable packet capture:
```bash
sudo python bluetooth_security_toolkit.py --capture --duration 30
```

### Command Line Options

- `--duration`: Scan duration in seconds (default: 10)
- `--verbose`: Enable verbose output for detailed logging
- `--attack`: Enable active attack mode
- `--capture`: Enable packet capture

## Output

The tool generates three types of output:
1. Real-time console output with color-coded information
2. Detailed log files:
   - `bluetooth_scan_[timestamp].log`: Technical scan details
   - `security_report_[timestamp].txt`: Comprehensive security assessment report
3. Packet captures:
   - `bluetooth_capture_[timestamp].pcap`: Raw Bluetooth traffic

## Attack Capabilities

### MITM Attacks
- Intercepts and manipulates Bluetooth communications
- Uses Bettercap's BLE module for sophisticated MITM
- Can modify data in transit

### Device Spoofing
- Impersonates legitimate Bluetooth devices
- Can clone device identities
- Enables unauthorized pairing attempts

### DoS Attacks
- Floods targets with pairing requests
- Performs Bluetooth signal jamming
- Disrupts existing connections

### Encryption Attacks
- Tests for weak encryption
- Attempts encryption downgrade
- Checks for KNOB attack vulnerability

## Security Considerations

- This tool should only be used on devices you own or have explicit permission to test
- Some features require root/administrator privileges
- Active attacks can disrupt legitimate Bluetooth communications
- Always follow local laws and regulations regarding Bluetooth scanning and testing
- Use the attack capabilities responsibly and ethically

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and security research purposes only. Users are responsible for complying with applicable laws and regulations. The authors are not responsible for any misuse or damage caused by this tool. The active attack capabilities should only be used in controlled testing environments with explicit permission. 