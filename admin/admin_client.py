# === admin/admin_client.py ===

import socket
import os
import time
from tqdm import tqdm
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.auth import SERVER_SECRET
from shared.network import scan_subnet

PORT = 9999
CHUNK_SIZE = 65536

cached_clients = []

def select_clients():
    print("Select clients:")
    for idx, ip in enumerate(cached_clients):
        print(f"[{idx}] {ip}")
    indices = input("Enter indices (comma-separated): ").strip()
    selected = []
    for i in indices.split(','):
        try:
            selected.append(cached_clients[int(i.strip())])
        except:
            continue
    return selected

def send_command(client_ip, command):
    try:
        s = socket.socket()
        s.connect((client_ip, PORT))

        if s.recv(1024).decode().startswith("TOKEN"):
            s.sendall(SERVER_SECRET.encode())
        if s.recv(1024).decode() != "AUTH_SUCCESS":
            print("❌ Auth failed.")
            return

        s.sendall(command.encode())
        output = s.recv(4096).decode()
        return f"[{client_ip}]\n{output}\n"
    except Exception as e:
        return f"❌ Error on {client_ip}: {e}"

def upload_file_to_client(client_ip, file_path):
    try:
        filesize = os.path.getsize(file_path)
        filename = os.path.basename(file_path)

        s = socket.socket()
        s.connect((client_ip, PORT))

        if s.recv(1024).decode().startswith("TOKEN"):
            s.sendall(SERVER_SECRET.encode())
        if s.recv(1024).decode() != "AUTH_SUCCESS":
            print("❌ Auth failed.")
            return

        s.sendall("upload".encode())
        s.recv(1024)
        s.sendall(filename.encode())
        s.recv(1024)
        s.sendall(str(filesize).encode())
        s.recv(1024)

        with open(file_path, "rb") as f:
            progress = tqdm(total=filesize, unit='B', unit_scale=True, desc=f"📤 {client_ip}: Uploading {filename}")
            while True:
                bytes_read = f.read(CHUNK_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
        progress.close()

        print(s.recv(1024).decode())
        s.close()

    except Exception as e:
        print(f"❌ Upload failed for {client_ip}: {e}")

def download_file_from_client(client_ip, remote_path, save_dir="downloads"):
    try:
        s = socket.socket()
        s.connect((client_ip, PORT))

        if s.recv(1024).decode().startswith("TOKEN"):
            s.sendall(SERVER_SECRET.encode())
        if s.recv(1024).decode() != "AUTH_SUCCESS":
            print("❌ Auth failed.")
            return

        s.sendall("download".encode())
        s.recv(1024)
        s.sendall(remote_path.encode())

        file_meta = s.recv(1024).decode()
        if file_meta.startswith("ERROR"):
            print(f"[{client_ip}] ❌ {file_meta}")
            return

        filesize = int(file_meta)
        s.sendall(b"READY")

        filename = os.path.basename(remote_path)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{client_ip.replace('.', '_')}_{filename}")

        with open(save_path, "wb") as f:
            received = 0
            progress = tqdm(total=filesize, unit='B', unit_scale=True, desc=f"📥 {client_ip}: Downloading {filename}")
            while received < filesize:
                chunk = s.recv(CHUNK_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
                progress.update(len(chunk))
            progress.close()

        print(f"✅ Saved to {save_path}")
        s.close()

    except Exception as e:
        print(f"❌ Download error from {client_ip}: {e}")

def menu():
    print("""
📦 Remote Admin Toolkit
----------------------------
[1] List Online Clients                 [2] Send Command to Selected Clients
[3] Broadcast Command to All Clients    [4] Upload File to a Client
[5] Download File from a Client         [6] Get System Info from Client
[7] Capture Screenshot from Client      [8] List Files in Directory (on Client)
[9] Open App on Client (e.g., Chrome)   [H] Help
[0] Exit
""")

def help_section():
    print("""
ℹ️  Help - Remote Admin Toolkit

[1] List Online Clients
    → Scans the LAN for devices running the client.

[2] Send Command to Selected Clients
    → Select from indexed list of online clients and send a command.

[3] Broadcast Command to All Clients
    → Same as above, but auto-sent to all online clients.

[4] Upload File
    → Select file path from your system. Client will receive the file.

[5] Download File
    → You provide full path of a file on the client machine to fetch.

[6] Get System Info
    → Fetches system configuration, OS, memory, etc.

[7] Capture Screenshot
    → Captures screenshot from client and saves as .png.

[8] List Files
    → Works like 'ls' (Linux/mac) or 'dir' (Windows).

[9] Open App on Client
    → Common examples:
       - start chrome
       - start notepad
       - start "" "C:\\Path\\To\\App.exe"

[0] Exit
    → Cleanly exits the tool.

🔐 Tip: Make sure client is running and connected to same network.
""")

if __name__ == "__main__":
    while True:
        menu()
        choice = input("Enter choice: ").strip().lower()

        if choice == "1":
            cached_clients = scan_subnet()
            print("Online Clients:")
            for idx, ip in enumerate(cached_clients):
                print(f"[{idx}] {ip}")

        elif choice == "2":
            if not cached_clients:
                print("⚠️  Run option 1 first to scan clients.")
                continue
            selected = select_clients()
            cmd = input("Enter command: ")
            for ip in selected:
                print(send_command(ip, cmd))

        elif choice == "3":
            if not cached_clients:
                cached_clients = scan_subnet()
            cmd = input("Enter command to broadcast: ")
            for ip in cached_clients:
                print(send_command(ip, cmd))

        elif choice == "4":
            if not cached_clients:
                print("⚠️  Run option 1 first to scan clients.")
                continue
            selected = select_clients()
            path = input("Path to file: ")
            for ip in selected:
                upload_file_to_client(ip, path)

        elif choice == "5":
            if not cached_clients:
                print("⚠️  Run option 1 first to scan clients.")
                continue
            selected = select_clients()
            remote_path = input("Remote file path: ")
            for ip in selected:
                download_file_from_client(ip, remote_path)

        elif choice == "6":
            if not cached_clients:
                print("⚠️  Run option 1 first to scan clients.")
                continue
            selected = select_clients()
            for ip in selected:
                print(send_command(ip, "sysinfo"))

        elif choice == "7":
            if not cached_clients:
                print("⚠️  Run option 1 first to scan clients.")
                continue
            selected = select_clients()
            for ip in selected:
                print(send_command(ip, "screenshot"))

        elif choice == "8":
            if not cached_clients:
                print("⚠️  Run option 1 first to scan clients.")
                continue
            selected = select_clients()
            folder = input("Folder path: ")
            for ip in selected:
                print(send_command(ip, f"ls {folder}"))

        elif choice == "9":
            if not cached_clients:
                print("⚠️  Run option 1 first to scan clients.")
                continue
            selected = select_clients()
            app_cmd = input("Enter launch command (e.g., start chrome): ")
            for ip in selected:
                print(send_command(ip, app_cmd))

        elif choice == "h":
            help_section()

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("❌ Invalid choice. Press H for help.")
