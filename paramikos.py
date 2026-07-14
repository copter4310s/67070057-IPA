import time
import paramiko

def main():
    user = "admin"
    device_ips = ["172.31.57.1", "172.31.57.2",
                  "172.31.57.3", "172.31.57.4",
                  "172.31.57.5"]

    for ip in device_ips:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=user, key_filename="C:\\Users\\Administrator\\Documents\\cisco\\admin_open.private")

        stdin, stdout, stderr = client.exec_command('show ip int br')
        print(stdout.read().decode())
        print(stderr.read().decode())
        client.close()

main()
