import _thread as thread
import time

import websocket

from utils.mirai_api import mirai
from utils.msg_manager import msg_manager


def on_message(_, message):
    msg_manager(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("closed")


def on_open(ws):
    def run(*args):
        time.sleep(1)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    url = f"{mirai.ws}/all?verifyKey={mirai.key}&sessionKey={mirai.session}&qq={mirai.qq}"
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url=url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
