# Bluetooth Security Assessment Toolkit

A comprehensive Bluetooth security assessment tool that performs device discovery, vulnerability scanning, and security analysis for both Classic Bluetooth and BLE devices.

## Features

- Device Discovery & Enumeration
  - Scans for both Classic Bluetooth and BLE devices
  - Extracts device metadata (MAC addresses, names, signal strength)
  - Classifies devices based on type and manufacturer

- Active & Passive Reconnaissance
  - Intercepts BLE advertising packets
  - Enumerates available services and UUIDs
  - Monitors connection parameters

- Security Analysis
  - Tests for common vulnerabilities
  - Detects weak configurations
  - Identifies potential attack vectors

- Detailed Reporting
  - Generates comprehensive security reports
  - Provides actionable remediation advice
  - Logs all findings with timestamps

## Prerequisites

- Python 3.7+
- Linux-based system (some features require root privileges)
- Bluetooth adapter supporting both Classic and BLE

### System Dependencies

For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev bluetooth libbluetooth-dev
```

For Fedora/RHEL:
```bash
sudo dnf install python3-devel bluetooth bluez-libs-devel
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

### Command Line Options

- `--duration`: Scan duration in seconds (default: 10)
- `--verbose`: Enable verbose output for detailed logging

## Output

The tool generates two types of output:
1. Real-time console output with color-coded information
2. Detailed log files:
   - `bluetooth_scan_[timestamp].log`: Technical scan details
   - `security_report_[timestamp].txt`: Comprehensive security assessment report

## Security Considerations

- This tool should only be used on devices you own or have explicit permission to test
- Some features require root/administrator privileges
- Always follow local laws and regulations regarding Bluetooth scanning and testing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and security research purposes only. Users are responsible for complying with applicable laws and regulations. The authors are not responsible for any misuse or damage caused by this tool. 