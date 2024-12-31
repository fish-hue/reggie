```markdown
# A Windows Registry Information Gathering Tool

This Python script collects various system information from a Windows machine and generates
a report that includes details about installed software, network adapters,
mapped network drives, USB devices, firewall status, and more. The script pulls data from
the Windows Registry and other system utilities to gather relevant information.

## Features

The script retrieves the following system information:

- **OS Information** (e.g., Windows version)
- **Install Date** and **Registered Owner** of Windows
- **Mapped Network Drives** (i.e., currently mapped drives)
- **USB Devices** (currently connected USB devices)
- **Firewall Status** (for all profiles)
- **Installed Software** (software listed in the Windows Registry)
- **Network Adapters** (including DHCP status, IP addresses, etc.)
- **IP Forwarding Status**
- **Time Zone setting**

Results are displayed in the terminal or command prompt.

## Requirements

- Python 3.x
- Windows operating system (for registry access and system utilities)

## Installation

1. Clone or download the repository to your local machine:

   ```bash
   git clone https://github.com/fish-hue/reggie.git
   ```

2. Navigate to the directory containing the script:

   ```bash
   cd reggie/system-information-collector
   ```

3. Install any required dependencies (if any, but currently none).

## Usage

1. Open a command prompt (or terminal) with administrative privileges.
2. Run the script using Python:

   ```bash
   python reggie.py
   ```

The script will:
- Collect system information.
- Display the results in the terminal.

## Example Output

After running the script, you will see a summary of the collected data in the terminal:

```yaml
--- System Information ---
OS Information:
  Windows 10 Pro

Date of Install:
  2022-01-01

Registered Owner:
  John Doe

System Root:
  C:\Windows

Time Zone:
  UTC-05:00

Mapped Network Drives:
  - Z: \\network\share

USB Devices:
  - DeviceID: 12345
  - Description: USB Keyboard

IP Forwarding Status:
  IP Forwarding is Disabled

Firewall Status:
  - Domain: Enabled
  - Private: Enabled
  - Public: Disabled

Installed Software:
  - Mozilla Firefox (x64 en-US)
  - Microsoft Visual C++ 2022 Runtime
  - VMware Tools

Network Adapters:
  - Adapter: Ethernet
    DHCPEnabled: Yes
    IPAddress: 192.168.1.2
    SubnetMask: 255.255.255.0
    DefaultGateway: 192.168.1.1

Current User:
  john_doe
```

## Notes

- Running the script with administrator privileges is required to access certain registry values and run system utilities like `netsh` and `wmic`.
- Some system information may not be available depending on user permissions or system configurations.
```
