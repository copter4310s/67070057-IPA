from netmiko import ConnectHandler

def main():
    username = "admin"
    device_ip = "172.31.57.3"
    device_params = {"device_type": "cisco_ios",
                     "ip": device_ip,
                     "username": username,
                     "key_file": "C:\\Users\\Administrator\\Documents\\cisco\\admin_open.private",
                     "disabled_algorithms": {"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]}
                     }

    with ConnectHandler(**device_params) as ssh:
        ssh.send_command("en")
        ssh.send_command("conf t")
        ssh.send_command("vlan 101")
        ssh.send_command("exit")
        ssh.send_command("int range gi0/1 - 2")
        ssh.send_command("switchport mode access")
        ssh.send_command("switchport access vlan 101")
        ssh.send_command("end")
        result = ssh.send_command("show vlan")
        print(result)

main()
