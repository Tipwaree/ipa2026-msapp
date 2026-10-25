import json

from bson import json_util

from database import save_interface_status
from router_client import get_interfaces


def callback(ch, method, props, body):
    try:
        job = json_util.loads(body.decode())
    except Exception as e:
        # message เก่าที่ไม่ใช่ JSON (เช่น 192.168.1.44 จากตอน Part 7)
        # จะไม่ทำให้ consumer ค้าง
        print(f"Skipped message that is not JSON: {body!r} ({e})", flush=True)
        return

    router_ip = job["ip"]
    router_username = job["username"]
    router_password = job["password"]

    print(f"Received job for router {router_ip}", flush=True)
    try:
        output = get_interfaces(router_ip, router_username, router_password)
        print(json.dumps(output, indent=2), flush=True)
        save_interface_status(router_ip, output)  # Part 12
        print(f"Stored interface status for {router_ip}", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
