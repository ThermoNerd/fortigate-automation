from fortiosapi import FortiOSAPI
from netmiko import ConnectHandler
from napalm import get_network_driver
from rich.console import Console
from rich.table import Table
import json
import sys
import logging
import time
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
console = Console()

class NetworkDevice:
    def __init__(self, hostname: str, device_type: str, username: str, password: str):
        self.hostname = hostname
        self.device_type = device_type
        self.username = username
        self.password = password
        self.connection = None

    def connect(self) -> bool:
        """Establish connection to the device"""
        try:
            device_info = {
                'device_type': self.device_type,
                'host': self.hostname,
                'username': self.username,
                'password': self.password,
            }
            self.connection = ConnectHandler(**device_info)
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {self.hostname}: {str(e)}")
            return False

    def send_command(self, command: str) -> str:
        """Send a command to the device"""
        try:
            output = self.connection.send_command(command)
            return output
        except Exception as e:
            logger.error(f"Error sending command to {self.hostname}: {str(e)}")
            return ""

    def disconnect(self):
        """Safely disconnect from the device"""
        if self.connection:
            self.connection.disconnect()

class FortiGateDevice:
    def __init__(self, host: str, username: str, password: str, verify: bool = False):
        self.host = host
        self.username = username
        self.password = password
        self.verify = verify
        self.fgt = FortiOSAPI()

    def connect(self) -> bool:
        """Connect to FortiGate device"""
        try:
            self.fgt.login(self.host, self.username, self.password, verify=self.verify)
            return True
        except Exception as e:
            logger.error(f"Failed to connect to FortiGate {self.host}: {str(e)}")
            return False

    def get_system_status(self) -> Dict:
        """Get system status information"""
        try:
            return self.fgt.monitor('system', 'firmware')
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {}

    def get_interfaces(self) -> Dict:
        """Get network interface information"""
        try:
            return self.fgt.monitor('system', 'interface')
        except Exception as e:
            logger.error(f"Error getting interfaces: {str(e)}")
            return {}

    def get_firewall_policies(self) -> Dict:
        """Get firewall policies"""
        try:
            return self.fgt.get('firewall', 'policy')
        except Exception as e:
            logger.error(f"Error getting firewall policies: {str(e)}")
            return {}

    def disconnect(self):
        """Safely disconnect from the device"""
        try:
            self.fgt.logout()
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")

def display_device_info(device_info: Dict[str, Any]):
    """Display device information in a formatted table"""
    table = Table(title="Device Information")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    for key, value in device_info.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=2)
        table.add_row(str(key), str(value))

    console.print(table)

def backup_config(device: NetworkDevice, backup_path: str):
    """Backup device configuration"""
    try:
        if device.device_type.startswith('cisco'):
            config = device.send_command('show running-config')
        elif device.device_type.startswith('juniper'):
            config = device.send_command('show configuration | display set')
        else:
            config = device.send_command('show configuration')

        filename = f"{device.hostname}_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(f"{backup_path}/{filename}", 'w') as f:
            f.write(config)
        logger.info(f"Configuration backed up to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error backing up configuration: {str(e)}")
        return False

def main():
    # Example device configurations
    fortigate_config = {
        'host': 'https://YOUR_FORTIGATE_IP',
        'username': 'admin',
        'password': 'YOUR_PASSWORD'
    }

    cisco_config = {
        'hostname': 'YOUR_CISCO_IP',
        'device_type': 'cisco_ios',
        'username': 'admin',
        'password': 'YOUR_PASSWORD'
    }

    try:
        # FortiGate device operations
        console.print("[bold blue]Connecting to FortiGate device...[/bold blue]")
        fgt_device = FortiGateDevice(**fortigate_config)
        if fgt_device.connect():
            # Get FortiGate information
            system_status = fgt_device.get_system_status()
            interfaces = fgt_device.get_interfaces()
            policies = fgt_device.get_firewall_policies()

            # Display information
            if system_status:
                display_device_info({"System Status": system_status})
            if interfaces:
                display_device_info({"Interfaces": interfaces})
            if policies:
                display_device_info({"Firewall Policies": policies})

            fgt_device.disconnect()

        # Network device operations
        console.print("[bold blue]Connecting to network device...[/bold blue]")
        network_device = NetworkDevice(**cisco_config)
        if network_device.connect():
            # Example commands
            version = network_device.send_command('show version')
            interfaces = network_device.send_command('show ip interface brief')

            # Display information
            display_device_info({
                "Version Info": version,
                "Interface Status": interfaces
            })

            # Backup configuration
            backup_config(network_device, './backups')
            network_device.disconnect()

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
