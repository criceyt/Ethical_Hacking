import socket
from concurrent.futures import ThreadPoolExecutor
target = "192.168.194.130"


for puerto in range(1, 65534):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)


    try:
        s.connect((target, puerto))
        print(f"[+] Puerto {puerto} abierto")
    except:
        pass
    finally:
        s.close()

print("Escaneo completado")

