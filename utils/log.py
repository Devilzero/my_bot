import os
import time
from platform import system

class Log():
    def __init__(self) -> None:
        self.log_dir = os.path.realpath(__file__+"/../../data/log/")
        self.color = {
            "debug": "34",
            "info": "32",
            "wring": "33",
            "error": "31"
        }
        self.cur_sys = system()

    def write_log(self, msg, level="info"):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        today = now_time.split()[0]

        today_log_dir = os.path.join(self.log_dir, today)
        message_log_dir = os.path.join(today_log_dir, "message")
        if not os.path.isdir(message_log_dir):
            os.makedirs(message_log_dir)

        all_log_file = os.path.join(today_log_dir, "all.log")
        if level in self.color:
            log_file = os.path.join(today_log_dir, f"{level}.log")
        else:
            log_file = os.path.join(message_log_dir, f"{level}.log")


        if self.cur_sys == "Windows":
            log_msg = f"[{now_time}][{str(level).upper()}] - {msg}\n"
        elif self.cur_sys == "Linux":
            log_msg = f"[{now_time}][\033[{self.color.get(level, '36')}m{str(level).upper()}\033[0m] - {msg}"
        print(log_msg)
        with open(all_log_file, "a", encoding="utf-8") as all_log,\
             open(log_file, "a", encoding="utf-8") as sub_log:
            all_log.write(log_msg)
            sub_log.write(log_msg)

    def debug(self, msg):
        self.write_log(msg, "debug")

    def info(self, msg):
        self.write_log(msg, "info")

    def wring(self, msg):
        self.write_log(msg, "wring")

    def error(self, msg):
        self.write_log(msg, "error")

log = Log()

if __name__ == "__main__":
    for i in range(100):
        log.info(f"哈哈哈哈{i}")
    for i in range(100):
        log.error(f"哈哈哈哈{i}")
        log.write_log(f"哈哈哈哈{i}", "123456")