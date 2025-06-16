# FortiOS Network Automation

This project provides Python scripts for automating FortiGate device management using the FortiOS API.

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Configure your environment:
   - Open `forti_automation.py`
   - Update the following variables with your FortiGate details:
     - `host`: Your FortiGate device's IP address
     - `username`: Your FortiGate admin username
     - `password`: Your FortiGate admin password

## Usage

Run the script:
```bash
python forti_automation.py
```

The script will:
1. Connect to your FortiGate device
2. Retrieve system status information
3. Get interface details
4. Display the information in JSON format

## Features

- FortiGate device connection management
- System status monitoring
- Network interface information retrieval
- Secure API communication

## Requirements

- Python 3.6+
- fortiosapi
- requests
- cryptography

## Note

Make sure to:
- Use HTTPS for secure communication
- Replace placeholder credentials with your actual FortiGate device details
- Ensure network connectivity to your FortiGate device
