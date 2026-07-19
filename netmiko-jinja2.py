from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("templates"))

def get_device(dev_name):
    dev_list = {"R0": "172.31.57.1", "S0": "172.31.57.2", "S1": "172.31.57.3",
                "R1": "172.31.57.4", "R2": "172.31.57.5"}

    return {"device_type": "cisco_ios",
            "ip": dev_list[dev_name],
            "username": "admin",
            "key_file": "C:\\Users\\Administrator\\Documents\\cisco\\admin_open.private",
            "disabled_algorithms": {"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
            }

def render_config(template_name, **kwargs):
    template = env.get_template(template_name)
    rendered = template.render(**kwargs)
    return [line for line in rendered.splitlines() if line.strip()]

def main():
    # Config VLAN 101 on S1 and assign to interfaces
    with ConnectHandler(**get_device("S1")) as ssh:
        config = render_config("s1.j2",
                                  vlan_id="101",
                                  acl_permit1="10.50.3.0",
                                  acl_permit2="172.31.57.0")
        ssh.send_config_set(config)

        result = ssh.send_command("show vlan")
        print("+--- Switch 1 Result ---+")
        print(result)

    # Create loopback interface, config OSPF routing and ACL to SSH on R1
    with ConnectHandler(**get_device("R1")) as ssh:
        config = render_config("r1.j2",
                               loopback_ip="192.168.57.100",
                               net1="20.57.1.0",
                               net_link="20.57.99.0",
                               acl_permit1="10.50.3.0",
                               acl_permit2="172.31.57.0")
        ssh.send_config_set(config)
        
        result = ssh.send_command("show ip route vrf internet")
        print("\n+--- Router 1 Result ---+")
        print(result)

    # Create loopback interface, config OSPF routing, config PAT and ACL to SSH on R2
    with ConnectHandler(**get_device("R2")) as ssh:
        config = render_config("r2.j2",
                                  loopback_ip="192.168.57.101",
                                  net1="20.57.2.0",
                                  net_link="20.57.99.0",
                                  acl_permit1="10.50.3.0",
                                  acl_permit2="172.31.57.0")
        ssh.send_config_set(config)
        
        result = ssh.send_command("show ip route vrf internet")
        print("\n+--- Router 2 Result ---+")
        print(result)

main()
