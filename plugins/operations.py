import time
import platform
import psutil
from utils.mirai_api import mirai

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return f'{value:.2f}{s}'
    return f"{n}B"

def get_hw_info():
    cpu_percent = psutil.cpu_percent(0)
    mem = psutil.virtual_memory()

    before = psutil.net_io_counters()
    time.sleep(1)
    now = psutil.net_io_counters()
    up_speed = now.bytes_sent - before.bytes_sent
    down_speed = now.bytes_recv - before.bytes_recv

    msg = f"{platform.system()}\n"\
          f"{platform.version()}\n"\
          f"{platform.processor()}\n"\
          f"CPU: {cpu_percent}%\n"\
          f"内存: {bytes2human(mem.used)} / {bytes2human(mem.total)} ({mem.percent}%)\n"

    for id in psutil.disk_partitions():
        if 'cdrom' in id.opts or id.fstype == '':
            continue
        disk_name = id.device.split(':')
        s = disk_name[0]
        disk_info = psutil.disk_usage(id.device)
        msg += f"{s}盘: {bytes2human(disk_info.free)} / {bytes2human(disk_info.total)} ({disk_info.percent}%)\n"
    msg += f"↑ {bytes2human(up_speed)}/s | ↓ {bytes2human(down_speed)}/s"
    return msg


hw = ["运行状态"]

cmd_head_list = [*hw]


def mk_msg(data_json):
    form_group_id = data_json['data']['sender']['group']['id']
    from_msg = data_json['data']['messageChain'][1]['text']
    rev_list = from_msg.split()

    if rev_list[0] in hw:
        mirai.send_group_message(form_group_id, get_hw_info(), "TXT")