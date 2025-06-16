from netmiko import ConnectHandler
from getpass import getpass
from rich.console import Console
from rich.table import Table
import sys
import time
from typing import Dict, Optional
from datetime import datetime

__version__ = "1.1.0"  # Added version tracking
from datetime import datetime
import os

console = Console()

def connect_to_fortigate(host, username, password):
    """
    Establish SSH connection to FortiGate device
    """
    device_info = {
        'device_type': 'fortinet',
        'host': host,
        'username': username,
        'password': password,
    }
    
    try:
        console.print("[yellow]Connecting to FortiGate...[/yellow]")
        connection = ConnectHandler(**device_info)
        return connection
    except Exception as e:
        console.print(f"[red]Error connecting to FortiGate: {str(e)}[/red]")
        return None

def get_system_status(connection) -> Optional[Dict]:
    """
    Get comprehensive system status information from FortiGate
    Returns: Dictionary with command outputs or None if error occurs
    """
    commands = {
        'System Status': 'get system status',
        'Performance': 'get system performance status',
        'Interfaces': 'get system interface physical',
        'CPU Usage': 'get system cpu status',
        'Memory Usage': 'get system memory status',
        'Active Sessions': 'get system session status',
        'HA Status': 'get system ha status',
        'Firmware': 'get system firmware',
        'License Status': 'get system status | grep License',
        'VPN Status': 'get vpn ipsec status',
        'Link Monitor': 'get system link-monitor status',
        'Resource Usage': 'diagnose sys top'
    }
    
    status_info = {}
    
    try:
        for description, command in commands.items():
            console.print(f"[yellow]Executing: {description} ({command})[/yellow]")
            try:
                output = connection.send_command(command, read_timeout=30)
                status_info[description] = output.strip()
                time.sleep(1)  # Prevent overwhelming the device
            except Exception as cmd_error:
                console.print(f"[red]Error executing {description}: {str(cmd_error)}[/red]")
                status_info[description] = "Command failed"
                
        return status_info
    except Exception as e:
        console.print(f"[red]Error in get_system_status: {str(e)}[/red]")
        return None

def display_status(status_info, save_to_file=True):
    """
    Display the status information in a formatted table and optionally save to file
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(logs_dir, f'fortigate_status_{timestamp}.txt')

    # Display on screen and write to file
    with open(filename, 'w') as f:
        for command, output in status_info.items():
            # Display on screen
            console.print(f"\n[blue]===== {command} =====[/blue]")
            console.print(output)
            
            # Write to file
            f.write(f"\n===== {command} =====\n")
            f.write(str(output) + "\n")
        
        console.print(f"\n[green]Status information saved to: {filename}[/green]")

def main():
    # FortiGate FG-60E IP address
    host = "192.168.10.1"
    
    # Get credentials from user
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    
    # Connect to the FortiGate
    connection = connect_to_fortigate(host, username, password)
    if not connection:
        sys.exit(1)
    
    try:
        # Get and display system status
        status_info = get_system_status(connection)
        if status_info:
            display_status(status_info)
        
    except Exception as e:
        console.print(f"[red]Error occurred: {str(e)}[/red]")
    finally:
        # Always disconnect
        console.print("[yellow]Disconnecting from FortiGate...[/yellow]")
        connection.disconnect()
        console.print("[green]Disconnected successfully[/green]")

if __name__ == "__main__":
    main()
