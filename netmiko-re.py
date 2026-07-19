from netmiko import ConnectHandler
import re

def get_device(dev_name):
    dev_list = {"R0": "172.31.57.1", "S0": "172.31.57.2", "S1": "172.31.57.3",
                "R1": "172.31.57.4", "R2": "172.31.57.5"}

    return {"device_type": "cisco_ios",
            "ip": dev_list[dev_name],
            "username": "admin",
            "key_file": "C:\\Users\\Administrator\\Documents\\cisco\\admin_open.private",
            "disabled_algorithms": {"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
            }

def get_info(dev_name):
    with ConnectHandler(**get_device(dev_name)) as ssh:
        uptime = ssh.send_command("show version | include uptime")
        uptime_res = re.search(" \d+ \w+", uptime)
        result = ssh.send_command("show ip int br")
        match = re.findall("(\S+).*up.*up", result)
        print(f"+--- {dev_name} Information ---+")
        print(f"  Uptime:{uptime_res.group()}")
        print(f"  Active interfaces: {", ".join(match)}")
        print()

def main():
    get_info("R1")
    get_info("R2")

main()
