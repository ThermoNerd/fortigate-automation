from netmiko import ConnectHandler
from getpass import getpass
from rich.console import Console
from rich.table import Table
import sys
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

def get_system_status(connection):
    """
    Get system status information from FortiGate
    """
    commands = [
        'get system status',
        'get system performance status',
        'get system interface physical',
        'diagnose sys session status'
    ]
    
    status_info = {}
    
    try:
        for command in commands:
            console.print(f"[yellow]Executing: {command}[/yellow]")
            output = connection.send_command(command)
            status_info[command] = output
        return status_info
    except Exception as e:
        console.print(f"[red]Error getting system status: {str(e)}[/red]")
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
