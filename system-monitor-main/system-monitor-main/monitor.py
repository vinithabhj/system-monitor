import psutil
import platform
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init()

def read_config():
    """Read configuration from config.txt file."""
    config = {}
    try:
        with open('config.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        print(f"{Fore.RED}Error: config.txt file not found!{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error reading config file: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def get_color_for_percentage(percentage):
    """Return appropriate color based on usage percentage."""
    if percentage < 60:
        return Fore.GREEN
    elif percentage < 80:
        return Fore.YELLOW
    else:
        return Fore.RED

def format_size(size_bytes):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0

def is_relevant_mount(mountpoint):
    """Check if the mountpoint is relevant for monitoring."""
    # Filter out system volumes and temporary mounts
    system_volumes = ['/System/Volumes/', '/private/var/vm', '/private/var/folders']
    return not any(mountpoint.startswith(vol) for vol in system_volumes)

def get_network_info():
    """Get network interface information."""
    net_io = psutil.net_io_counters()
    return {
        'bytes_sent': format_size(net_io.bytes_sent),
        'bytes_recv': format_size(net_io.bytes_recv),
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv
    }

def get_battery_info():
    """Get battery information if available."""
    if not hasattr(psutil, "sensors_battery"):
        return None
    
    battery = psutil.sensors_battery()
    if battery is None:
        return None
        
    return {
        'percent': battery.percent,
        'power_plugged': battery.power_plugged,
        'time_left': battery.secsleft if battery.secsleft != -2 else None
    }

def get_system_info(return_text=False):
    """Display comprehensive system information with color-coded output."""
    output_lines = []
    
    if not return_text:
        # Clear screen for better readability
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # Header
    header = f"{'='*20} System Health Summary {'='*20}"
    output_lines.append(header)
    output_lines.append("")
    
    # Current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output_lines.append(f"Time: {current_time}")
    output_lines.append("")

    # CPU Information
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_color = get_color_for_percentage(cpu_percent)
    output_lines.append(f"CPU Usage: {cpu_percent}%")
    output_lines.append(f"CPU Cores: {psutil.cpu_count()} (Physical: {psutil.cpu_count(logical=False)})")
    output_lines.append("")
    
    # Memory Information
    memory = psutil.virtual_memory()
    mem_color = get_color_for_percentage(memory.percent)
    output_lines.append("Memory Usage:")
    output_lines.append(f"  Total: {format_size(memory.total)}")
    output_lines.append(f"  Used:  {format_size(memory.used)} ({memory.percent}%)")
    output_lines.append(f"  Free:  {format_size(memory.available)}")
    output_lines.append("")

    # Battery Information
    battery = get_battery_info()
    if battery:
        output_lines.append("Battery Status:")
        output_lines.append(f"  Level: {battery['percent']}%")
        output_lines.append(f"  Power: {'Connected' if battery['power_plugged'] else 'Battery'}")
        if battery['time_left'] is not None:
            hours = battery['time_left'] // 3600
            minutes = (battery['time_left'] % 3600) // 60
            output_lines.append(f"  Time Left: {hours}h {minutes}m")
        output_lines.append("")

    # Network Information
    net_info = get_network_info()
    output_lines.append("Network Usage:")
    output_lines.append(f"  Sent:     {net_info['bytes_sent']} ({net_info['packets_sent']} packets)")
    output_lines.append(f"  Received: {net_info['bytes_recv']} ({net_info['packets_recv']} packets)")
    output_lines.append("")

    # Disk Information
    output_lines.append("Storage Status:")
    seen_devices = set()  # Track unique devices to avoid duplicates
    for partition in psutil.disk_partitions():
        try:
            if not is_relevant_mount(partition.mountpoint):
                continue
                
            usage = psutil.disk_usage(partition.mountpoint)
            # Skip if we've already seen this device
            if partition.device in seen_devices:
                continue
            seen_devices.add(partition.device)
            
            disk_color = get_color_for_percentage(usage.percent)
            output_lines.append(f"\nDrive: {partition.device}")
            output_lines.append(f"  Mount: {partition.mountpoint}")
            output_lines.append(f"  Total: {format_size(usage.total)}")
            output_lines.append(f"  Used:  {format_size(usage.used)} ({usage.percent}%)")
            output_lines.append(f"  Free:  {format_size(usage.free)}")
        except:
            continue

    # System Uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    output_lines.append(f"\nSystem Uptime: {str(uptime).split('.')[0]}")

    if return_text:
        return "\n".join(output_lines)
    else:
        # Print with colors
        print(f"{Fore.CYAN}{header}{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}Time:{Style.RESET_ALL} {current_time}\n")
        print(f"{Fore.WHITE}CPU Usage:{Style.RESET_ALL} {cpu_color}{cpu_percent}%{Style.RESET_ALL}")
        print(f"{Fore.WHITE}CPU Cores:{Style.RESET_ALL} {psutil.cpu_count()} (Physical: {psutil.cpu_count(logical=False)})")
        print(f"\n{Fore.WHITE}Memory Usage:{Style.RESET_ALL}")
        print(f"  Total: {format_size(memory.total)}")
        print(f"  Used:  {format_size(memory.used)} ({mem_color}{memory.percent}%{Style.RESET_ALL})")
        print(f"  Free:  {format_size(memory.available)}")
        
        if battery:
            print(f"\n{Fore.WHITE}Battery Status:{Style.RESET_ALL}")
            print(f"  Level: {battery['percent']}%")
            print(f"  Power: {'Connected' if battery['power_plugged'] else 'Battery'}")
            if battery['time_left'] is not None:
                hours = battery['time_left'] // 3600
                minutes = (battery['time_left'] % 3600) // 60
                print(f"  Time Left: {hours}h {minutes}m")

        print(f"\n{Fore.WHITE}Network Usage:{Style.RESET_ALL}")
        print(f"  Sent:     {net_info['bytes_sent']} ({net_info['packets_sent']} packets)")
        print(f"  Received: {net_info['bytes_recv']} ({net_info['packets_recv']} packets)")

        print(f"\n{Fore.WHITE}Storage Status:{Style.RESET_ALL}")
        for partition in psutil.disk_partitions():
            try:
                if not is_relevant_mount(partition.mountpoint):
                    continue
                    
                usage = psutil.disk_usage(partition.mountpoint)
                if partition.device in seen_devices:
                    continue
                seen_devices.add(partition.device)
                
                disk_color = get_color_for_percentage(usage.percent)
                print(f"\n{Fore.WHITE}Drive: {partition.device}{Style.RESET_ALL}")
                print(f"  Mount: {partition.mountpoint}")
                print(f"  Total: {format_size(usage.total)}")
                print(f"  Used:  {format_size(usage.used)} ({disk_color}{usage.percent}%{Style.RESET_ALL})")
                print(f"  Free:  {format_size(usage.free)}")
            except:
                continue

        print(f"\n{Fore.WHITE}System Uptime:{Style.RESET_ALL} {str(uptime).split('.')[0]}")

def send_email_report(sender_email, sender_password, receiver_email, smtp_server="smtp.gmail.com", smtp_port=587):
    """Send system report via email."""
    # Get system info as text
    report_text = get_system_info(return_text=True)
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"System Health Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Add report text
    msg.attach(MIMEText(report_text, 'plain'))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        print("Email report sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def continuous_monitor(interval=2):
    """Continuously monitor system with specified refresh interval in seconds."""
    try:
        while True:
            get_system_info()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

def main():
    # Get email configuration
    config = read_config()
    sender_email = config.get('SENDER_EMAIL')
    email_password = config.get('EMAIL_PASSWORD')
    receiver_email = config.get('RECEIVER_EMAIL')

    if not all([sender_email, email_password, receiver_email]):
        print(f"{Fore.RED}Error: Missing email configuration in config.txt{Style.RESET_ALL}")
        sys.exit(1)

    # Get system information
    cpu_usage = get_system_info()
    memory_usage = get_system_info()
    battery_status = get_system_info()
    network_usage = get_network_info()
    storage_status = get_system_info()
    uptime = get_system_info()

    # Create email content
    email_content = f"""
    System Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ============================================

    CPU Usage:
    {cpu_usage}

    Memory Usage:
    {memory_usage}

    Battery Status:
    {battery_status}

    Network Usage:
    {network_usage}

    Storage Status:
    {storage_status}

    System Uptime:
    {uptime}
    """

    # Send email
    try:
        send_email_report(sender_email, email_password, receiver_email)
        print(f"{Fore.GREEN}Email sent successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error sending email: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
