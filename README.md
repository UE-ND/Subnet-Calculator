# Subnet Calculator 🔢

A Python script that calculates detailed subnet information from an IP address in CIDR notation.

## 🚀 Usage
```bash
python3 SubCalc.py [IP_ADDRESS]/[CIDR]

Example
Input:
python3 SubCalc.py 172.16.35.123/20

Output:
IP Address Class:   B
CIDR Notation:      /20
Subnet Mask:        255.255.240.0
Network Address:    172.16.32.0
Broadcast Address:  172.16.47.255
First Usable Host:  172.16.32.1
Last Usable Host:   172.16.47.254
Usable Hosts:       4094

Features
Calculates subnet mask, network/broadcast addresses

Identifies first/last usable hosts

Supports all IPv4 classes (A, B, C)

Handles custom CIDR ranges (1-32)

Error handling for invalid inputs

How It Works
Parses input (e.g., 192.168.1.10/24)

Converts IP to binary format

Performs bitwise operations to derive network properties

Validates IP class and host ranges

Outputs human-readable network details

📁 Requirements
Python 3.6+
