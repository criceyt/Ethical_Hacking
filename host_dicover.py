import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor


def ping_host(ip):
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", str(ip)],stdout=subprocess.DEVNULL)
        if result.returncode == 0:
                print(f"[+] Host activo: {ip}")
    except:
        pass
    

def main():
    network = ipaddress.ip_network("192.168.194.0/24", strict=False)

    print(f"[+] Escaneando red: {network}")
    print("-"* 40)
    with ThreadPoolExecutor(max_workers=50) as executor:
        for ip in network.hosts():
            executor.submit(ping_host, ip)

if __name__ == "__main__":
    main()