import winreg
import subprocess
import getpass
import os

def get_registry_value(path, name="", hkey=winreg.HKEY_LOCAL_MACHINE):
    """Fetch a registry value."""
    try:
        with winreg.OpenKey(hkey, path) as key:
            if name:
                value, regtype = winreg.QueryValueEx(key, name)
                return value
            else:
                values = {}
                num_values = winreg.QueryInfoKey(key)[1]
                for i in range(num_values):
                    value_name, value_data, _ = winreg.EnumValue(key, i)
                    values[value_name] = value_data
                return values
    except (OSError, FileNotFoundError) as e:
        return f"Error: {e}"

def get_mapped_network_drives():
    """Fetch network connections for mapped drives."""
    try:
        drive_info = subprocess.check_output("net use", shell=True, text=True)
        drives = [line.strip() for line in drive_info.splitlines() if line.strip() and line.startswith("\\")]
        return drives if drives else ["No mapped network drives found."]
    except subprocess.CalledProcessError as e:
        return ["Error retrieving mapped network drives: " + str(e)]

def get_usb_devices():
    """Fetch a list of connected USB devices with more details."""
    try:
        # Using a more detailed WMIC command to list USB devices
        output = subprocess.check_output("wmic path Win32_USBHub get DeviceID, PNPDeviceID, Description", shell=True, text=True)
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        
        # Skip headers and list USB devices
        devices = lines[1:] if len(lines) > 1 else ["No USB devices found."]
        return devices
    except Exception as e:
        return ["Error retrieving USB devices: " + str(e)]

def get_firewall_status():
    """Fetch the firewall status using netsh command."""
    try:
        output = subprocess.check_output("netsh advfirewall show allprofiles", shell=True, text=True)
        lines = output.splitlines()
        status = []
        for line in lines:
            # Capture all profile settings and states
            if "State" in line or "Profile" in line:
                status.append(line.strip())
        return status if status else ["No firewall status found."]
    except subprocess.CalledProcessError as e:
        return ["Error retrieving firewall status: " + str(e)]

def get_ip_forwarding_status():
    """Get IP Forwarding status."""
    ip_forwarding = get_registry_value(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "IPEnableRouter")
    if ip_forwarding == 1:
        return "IP Forwarding is Enabled"
    elif ip_forwarding == 0:
        return "IP Forwarding is Disabled"
    else:
        return "IP Forwarding status not found."

def get_network_adapters():
    """Fetch details of network adapters."""
    adapters = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces") as interfaces_key:
            num_subkeys = winreg.QueryInfoKey(interfaces_key)[0]
            for i in range(num_subkeys):
                adapter_name = winreg.EnumKey(interfaces_key, i)
                adapter_path = fr"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{adapter_name}"  # Use raw string
                adapter_values = get_registry_value(adapter_path, hkey=winreg.HKEY_LOCAL_MACHINE)
                
                if adapter_values:
                    adapter_info = f"Adapter: {adapter_name}"
                    for key, value in adapter_values.items():
                        adapter_info += f"\n  {key}: {value}"  # Add properties for each adapter
                    adapters.append(adapter_info)
    except Exception as e:
        return ["Error retrieving network adapters: " + str(e)]

    return adapters if adapters else ["No network adapters found."]

def get_installed_software():
    """Get installed software from registry."""
    software = []    
    try:
        # Check all relevant registry keys for installed software
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",  # For 32-bit apps
            r"Software\Microsoft\Windows\CurrentVersion\Uninstall",  # Current User software
        ]

        for path in registry_paths:
            for hkey in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                try:
                    with winreg.OpenKey(hkey, path) as key:
                        num_subkeys = winreg.QueryInfoKey(key)[0]
                        for i in range(num_subkeys):
                            subkey_name = winreg.EnumKey(key, i)
                            subkey_path = f"{path}\\{subkey_name}"
                            software_info = get_registry_value(subkey_path, hkey=hkey)
                            # Look specifically for the 'DisplayName' as a marker of installed software
                            if 'DisplayName' in software_info:
                                software.append(software_info['DisplayName'])
                except OSError:
                    continue

        return software if software else ["No software found in registry paths."]
    except Exception as e:
        return ["Error retrieving installed software: " + str(e)]

def write_report_to_file(results, filename="system_report.txt"):
    """Write the results to a text file in a user-friendly format."""
    with open(filename, "w") as f:
        f.write("--- System Information Report ---\n\n")
        for key, value in results.items():
            f.write(f"{key}:\n")
            if isinstance(value, list):
                for item in value:
                    f.write(f"  - {item}\n")  # Bullet points for list items
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    f.write(f"  {subkey}: {subvalue}\n")
            else:
                f.write(f"  {value}\n")
            f.write("\n")

def display_results(results):
    """Display results in a user-friendly format."""
    print("\n--- System Information ---\n")
    for key, value in results.items():
        print(f"{key}:")
        if isinstance(value, list):
            for item in value:
                print(f"  - {item}")
            print()
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                print(f"  {subkey}: {subvalue}")
            print()
        else:
            print(f"  {value}\n")

def main():
    results = {
        "OS Information": get_registry_value(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "ProductName"),
        "Date of Install": get_registry_value(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "InstallDate"),
        "Registered Owner": get_registry_value(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "RegisteredOwner"),
        "System Root": get_registry_value(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "SystemRoot"),
        "Time Zone": get_registry_value(r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation", "TimeZoneKeyName"),
        "Mapped Network Drives": get_mapped_network_drives(),
        "USB Devices": get_usb_devices(),
        "IP Forwarding Status": get_ip_forwarding_status(),
        "Firewall Status": get_firewall_status(),
        "Installed Software": get_installed_software(),  # Returns list of installed software
        "Network Adapters": get_network_adapters(),
        "Current User": getpass.getuser(),
    }

    # Display results in a user-friendly format
    display_results(results)

    # Write results to a text file
    write_report_to_file(results)

if __name__ == "__main__":
    main()
