import socket
import concurrent.futures
import ipaddress

PORT = 9999
TIMEOUT = 1  # seconds

# Automatically detect local subnet
def get_local_subnet():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    subnet = ".".join(local_ip.split(".")[:3])
    return subnet

# Try connecting to a single IP
def check_ip(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            sock.connect((ip, PORT))
        return ip
    except:
        return None

def scan_subnet():
    subnet = get_local_subnet()
    base_ip = subnet + ".{}"

    print(f"🔍 Scanning subnet {subnet}.0/24 on port {PORT}...\n")
    active_ips = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_ip, base_ip.format(i)) for i in range(1, 255)]
        for future in concurrent.futures.as_completed(futures):
            ip = future.result()
            if ip:
                print(f"✅ Client found: {ip}")
                active_ips.append(ip)

    return active_ips

import os

def save_ips(ips, filename=None):
    if filename is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, "connectionLogs", "ips.txt")
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        for ip in ips:
            f.write(ip + "\n")


if __name__ == "__main__":
    found_ips = scan_subnet()
    if found_ips:
        save_ips(found_ips)
        print(f"\n💾 Saved {len(found_ips)} IPs to admin/ips.txt")
    else:
        print("\n❌ No clients found.")

