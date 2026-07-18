from netmiko import ConnectHandler

def get_device(dev_name):
    dev_list = {"R0": "172.31.57.1", "S0": "172.31.57.2", "S1": "172.31.57.3",
                "R1": "172.31.57.4", "R2": "172.31.57.5"}

    return {"device_type": "cisco_ios",
            "ip": dev_list[dev_name],
            "username": "admin",
            "key_file": "C:\\Users\\Administrator\\Documents\\cisco\\admin_open.private",
            "disabled_algorithms": {"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
            }

def main():
    # Config VLAN 101 on S1 and assign to interfaces
    with ConnectHandler(**get_device("S1")) as ssh:
        ssh.send_config_set("vlan 101")
        ssh.send_config_set(["int range gi0/1 - 2",
                             "switchport mode access",
                             "switchport access vlan 101"])
        ssh.send_config_set(["ip access-list standard 9",
                             "permit 10.50.3.0 0.0.0.255",
                             "permit 172.31.57.0 0.0.0.15"])
        ssh.send_config_set(["line vty 0 4",
                             "access-class 9 in"])

        result = ssh.send_command("show vlan")
        print("+--- Switch 1 Result ---+")
        print(result)

    # Create loopback interface, config OSPF routing and ACL to SSH on R1
    with ConnectHandler(**get_device("R1")) as ssh:
        ssh.send_config_set(["int loopback 0",
                             "vrf forwarding internet",
                             "ip add 192.168.57.100 255.255.255.255",
                             "no shut"])
        ssh.send_config_set(["router ospf 1 vrf internet",
                             "network 20.57.1.0 0.0.0.255 area 0",
                             "network 20.57.99.0 0.0.0.3 area 0",
                             "network 192.168.57.100 0.0.0.0 area 0"])
        ssh.send_config_set(["ip access-list standard 9",
                             "permit 10.50.3.0 0.0.0.255",
                             "permit 172.31.57.0 0.0.0.15"])
        ssh.send_config_set(["line vty 0 4",
                             "access-class 9 in"])
        
        result = ssh.send_command("show ip route vrf internet")
        print("\n+--- Router 1 Result ---+")
        print(result)

    # Create loopback interface, config OSPF routing, config PAT and ACL to SSH on R2
    with ConnectHandler(**get_device("R2")) as ssh:
        ssh.send_config_set(["int loopback 0",
                             "vrf forwarding internet",
                             "ip add 192.168.57.101 255.255.255.255",
                             "no shut"])
        ssh.send_config_set(["router ospf 1 vrf internet",
                             "network 20.57.2.0 0.0.0.255 area 0",
                             "network 20.57.99.0 0.0.0.3 area 0",
                             "network 192.168.57.101 0.0.0.0 area 0",
                             "default-information originate always"])
        ssh.send_config_set(["int g0/3",
                             "ip ospf shutdown"])
        ssh.send_config_set(["int range g0/1 - 2",
                             "ip nat inside"])
        ssh.send_config_set(["int g0/3",
                             "ip nat outside"])
        ssh.send_config_set("access-list 8 permit any")
        ssh.send_config_set("ip nat inside source list 8 interface GigabitEthernet0/3 vrf internet overload")
        ssh.send_config_set(["ip access-list standard 9",
                             "permit 10.50.3.0 0.0.0.255",
                             "permit 172.31.57.0 0.0.0.15"])
        ssh.send_config_set(["line vty 0 4",
                             "access-class 9 in"])
        
        result = ssh.send_command("show ip route vrf internet")
        print("\n+--- Router 2 Result ---+")
        print(result)

main()
