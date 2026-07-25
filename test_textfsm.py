import re
import pytest
import textfsm
from netmiko import ConnectHandler
from textfsm_set import get_desc

def get_device(dev_name):
    dev_list = {"R0": "172.31.57.1", "S0": "172.31.57.2", "S1": "172.31.57.3",
                "R1": "172.31.57.4", "R2": "172.31.57.5"}

    return {"device_type": "cisco_ios",
            "ip": dev_list[dev_name],
            "username": "admin",
            "key_file": "C:\\Users\\Administrator\\Documents\\cisco\\admin_open.private",
            "disabled_algorithms": {"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
            }

@pytest.mark.parametrize(
    "input_data, output_data",
    [
        ("G0/0", "Connect to G0/1 of S0"),
        ("G0/1", "Connect to PC"),
        ("G0/2", "Connect to G0/1 of R2")
    ]
)
def test_r1(input_data, output_data):
    assert output_data == get_desc("R1", input_data)

@pytest.mark.parametrize(
    "input_data, output_data",
    [
        ("G0/0", "Connect to G0/2 of S0"),
        ("G0/1", "Connect to G0/2 of R1"),
        ("G0/2", "Connect to G0/1 of S1"),
        ("G0/3", "Connect to WAN")
    ]
)
def test_r2(input_data, output_data):
    assert output_data == get_desc("R2", input_data)

@pytest.mark.parametrize(
    "input_data, output_data",
    [
        ("G0/0", "Connect to G0/3 of S0"),
        ("G0/1", "Connect to G0/2 of R2"),
        ("G0/2", "Connect to PC")
    ]
)
def test_s1(input_data, output_data):
    assert output_data == get_desc("S1", input_data)

if __name__ == "__main__":
    print("pytest -v -s .\\test_textfsm.py")
