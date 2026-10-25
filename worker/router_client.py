import os

import ntc_templates
from netmiko import ConnectHandler


def normalize(rows):
    """ทำให้ key ตรงกับตัวอย่างอาจารย์ ไม่ว่า ntc-templates จะคืน intf/ipaddr หรือ interface/ip_address"""
    return [
        {
            "interface": r.get("interface", r.get("intf")),
            "ip_address": r.get("ip_address", r.get("ipaddr")),
            "status": r["status"],
            "proto": r["proto"],
        }
        for r in rows
    ]


def get_interfaces(ip, username, password):
    os.environ["NET_TEXTFSM"] = os.path.join(
        os.path.dirname(ntc_templates.__file__), "templates"
    )
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
    }
    with ConnectHandler(**device) as conn:
        conn.enable()
        result = conn.send_command("show ip int br", use_textfsm=True)
    return normalize(result)
