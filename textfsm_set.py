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

def get_desc(dev_name, port):
    with ConnectHandler(**get_device(dev_name)) as ssh:
        result = ssh.send_command(f"show int {port}", use_textfsm=True)
        return result[0]["description"]

def set_desc(dev_name, port, desc):
    with ConnectHandler(**get_device(dev_name)) as ssh:
        return ssh.send_config_set([f"int {port}", f"description {desc}"])

def main():
    # Config R1 Description
    for curr_dev in ["R1", "R2", "S1"]:
        with ConnectHandler(**get_device(curr_dev)) as ssh:
            cdp_res = ssh.send_command(f"show cdp neighbor", use_textfsm=True)
            for i in cdp_res:
                local_int = i["local_interface"].replace("ig ", "")
                neigh_int = "G" + i["neighbor_interface"]
                neigh_name = i["neighbor_name"].replace(".ipa.com", "")
                set_desc(curr_dev, local_int, f"Connect to {neigh_int} of {neigh_name}")
            
            if curr_dev == "R1":
                set_desc(curr_dev, "G0/1", "Connect to PC")
            
            if curr_dev == "R2":
                set_desc(curr_dev, "G0/3", "Connect to WAN")

            if curr_dev == "S1":
                set_desc(curr_dev, "G0/2", "Connect to PC")
    
    print("Set!")

main()
