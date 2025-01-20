import paramiko
import os
import time
import random

def generate_file(file_path):
    T = round(random.uniform(20.0, 30.0), 2)
    H = round(random.uniform(40.0, 60.0), 2)
    W = round(random.uniform(5.0, 15.0), 2)

    with open(file_path, 'w') as file:
        file.write(f"T : {T}\nH : {H}\nW : {W}\n")

def transfer_file(local_path, remote_path, hostname, username, password, port=22):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

        ssh.close()
        print(f"Fichier '{local_path}' transféré avec succès vers '{remote_path}'")
    except Exception as e:
        print(f"Erreur lors du transfert : {e}")

if __name__ == "__main__":
    HOSTNAME = "172.20.10.3"
    USERNAME = "1"
    PASSWORD = "147369"

    i = 1
    while True:
        local_file = f"/home/pi/data_{i}.txt"
        remote_file = f"C:/Users/1/Desktop/ConnectedNestingBox/web_site/project/app/static/data/data_{i}.txt"

        generate_file(local_file)
        transfer_file(local_file, remote_file, HOSTNAME, USERNAME, PASSWORD)

        i += 1
        time.sleep(2)
