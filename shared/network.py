import socket
import threading

def is_client_online(ip, port=9999, timeout=1):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

def scan_subnet(subnet="192.168.1.", port=9999):
    online = []
    threads = []

    def check(ip):
        if is_client_online(ip, port):
            online.append(ip)

    for i in range(1, 255):
        ip = f"{subnet}{i}"
        t = threading.Thread(target=check, args=(ip,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return online
