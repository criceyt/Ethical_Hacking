import socket
from concurrent.futures import ThreadPoolExecutor
import requests
target = "192.168.194.2"

def detect_http(target, puerto):
    try:
        url = f"http://{target}:{puerto}"
        r = requests.get(url, timeout=3, verify=False)
        server = r.headers.get("Server", "Desconocido")
        return f"HTTP -> {server}"
    except:
        return "HTTP -> No identificado"
    
def detect_https(target, puerto):
    try:
        url = f"https://{target}:{puerto}"
        r = requests.get(url, timeout=3, verify=False)
        server = r.headers.get("Server", "Desconocido")
        return f"HTTPS -> {server}"
    except:
        return "HTTPS -> No identificado"
    
def detect_banner(target, puerto):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((target, puerto))
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        if banner:
            return f"{banner}"
        else:
            return "Servicio detectado, sin banner"
    except:
        pass

def port_scan(target, puerto):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            s.connect((target, puerto))
            result = detect_service(target, puerto)
            print(f"[+] Puerto {puerto} -> {result}")
        except: 
            pass
        finally:
            s.close()

def detect_service(target, puerto):
    try:
        if puerto == 80:
            return detect_http(target, puerto)
        elif puerto == 443:
            return detect_https(target, puerto)
        else:
            return detect_banner(target, puerto)
    except:
        pass



with ThreadPoolExecutor(max_workers=80) as executor:
    for puerto in range (1, 65534):
        executor.submit(port_scan, target, puerto)