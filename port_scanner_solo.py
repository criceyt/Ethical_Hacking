import socket
from concurrent.futures import ThreadPoolExecutor
target = "192.168.194.130"

def port_scan(target, puerto):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    try:
        s.connect((target, puerto))
        print(f"[+] Puerto {puerto} abierto")
    except: 
        pass
    finally:
        s.close()


with ThreadPoolExecutor(max_workers=200) as executor:
    for puerto in range (1, 65534):
        executor.submit(port_scan, target, puerto)