from fortiosapi import FortiOSAPI
import json
import sys

def connect_to_fortigate(host, username, password, verify=False):
    """
    Establish connection to FortiGate device
    """
    fgt = FortiOSAPI()
    try:
        fgt.login(host, username, password, verify=verify)
        return fgt
    except Exception as e:
        print(f"Error connecting to FortiGate: {str(e)}")
        return None

def get_system_status(fgt):
    """
    Get system status information
    """
    try:
        status = fgt.monitor('system', 'firmware')
        return status
    except Exception as e:
        print(f"Error getting system status: {str(e)}")
        return None

def get_interfaces(fgt):
    """
    Get network interface information
    """
    try:
        interfaces = fgt.monitor('system', 'interface')
        return interfaces
    except Exception as e:
        print(f"Error getting interfaces: {str(e)}")
        return None

def main():
    # Replace these with your FortiGate device details
    host = "https://YOUR_FORTIGATE_IP"
    username = "admin"
    password = "YOUR_PASSWORD"
    
    # Connect to FortiGate
    fgt = connect_to_fortigate(host, username, password)
    if not fgt:
        sys.exit(1)
    
    try:
        # Get system status
        status = get_system_status(fgt)
        if status:
            print("\nSystem Status:")
            print(json.dumps(status, indent=2))
        
        # Get interface information
        interfaces = get_interfaces(fgt)
        if interfaces:
            print("\nInterface Information:")
            print(json.dumps(interfaces, indent=2))
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        # Always logout
        fgt.logout()

if __name__ == "__main__":
    main()
