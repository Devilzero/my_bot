import os
import requests

img_dir = os.path.realpath(__file__+"/../../data/img/")


class Mirai(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, qq, key, mirai_ip="localhost", mirai_port=8080) -> None:
        self.session = None
        self.qq = qq
        self.key = key
        self.url = f'http://{mirai_ip}:{mirai_port}'
        self.ws = f'ws://{mirai_ip}:{mirai_port}'
        self.get_version()
        self.verify()
        self.bind()
        self.start_web_socket()

    def get_version(self):
        url = self.url+'/about'
        res = requests.get(url=url)
        json_data = res.json()
        if json_data['data']['version']:
            print(f"当前版本：{json_data['data']['version']}")
        else:
            raise SystemExit('版本获取失败！')

    def verify(self):
        """
        获取授权信息
        """
        url = self.url+'/verify'
        request_data = {'verifyKey': self.key}
        res = requests.post(url=url, json=request_data)
        json_data = res.json()
        if json_data['code'] == 0:
            print('验证成功！')
            self.session = json_data['session']
            return 0
        else:
            raise SystemExit(
                f"验证失败: <{json_data['code']}> {request_data['authKey']}")

    def bind(self):
        """
        绑定QQ
        """
        request_data = {
            'sessionKey': self.session,
            'qq': self.qq
        }
        url = self.url+'/bind'
        res = requests.post(url=url, json=request_data)
        json_data = res.json()
        if json_data['code'] == 0:
            print('QQ绑定成功！')
        else:
            raise SystemExit('QQ绑定失败！')

    def release(self):
        """
        清楚当前sesson
        """
        request_data = {
            'sessionKey': self.session,
            'qq': self.qq
        }
        url = self.url+'/release'
        res = requests.post(url=url, json=request_data)
        json_data = res.json()
        if json_data['code'] == 0:
            print('清除成功！')
        else:
            raise SystemExit('清除失败！')

    def start_web_socket(self):
        request_data = {
            'sessionKey': self.session,
            "enableWebsocket": True
        }
        url = self.url+'/config'
        requests.post(url=url, json=request_data)
        print('WebSocketStarted!')

    def accept_new_friend(self, event_id, from_id, group_id, message, name):
        request_data = {
            'sessionKey': self.session,
            'eventId': int(event_id),
            'fromId': int(from_id),
            'groupId': int(group_id),
            'operate': 0,
            "message": message
        }
        url = self.url + '/resp/newFriendRequestEvent'
        res = requests.post(url=url, json=request_data)
        json_data = res.json()
        if json_data['code'] != 0:
            print("get error {} when send message".format(json_data['code']))
        else:
            print("got new friend request from {} with QQ:{}".format(from_id, name))

    def send_group_message(self, target, msg: str, message_type="TEXT", ATQQ=None):
        """
        向某群(target)发送消息(msg)
        target: 群号
        msg: 发送的内容
        message_type: 消息类型(TEXT、IMG)
        needAT: 是否需要@对方
        ATQQ: @ATQQ, 留空则不@
        """
        chain = []
        if ATQQ:
            temp = {"type": "At", "target": ATQQ, "display": "@来源"}
            chain.append(temp)
            temp = {"type": "Plain", "text": " "}
            chain.append(temp)
        if message_type == "TEXT":
            temp = {"type": "Plain", "text": msg}
            chain.append(temp)
        elif message_type == "IMG":
            img_path = os.path.join(img_dir, msg)
            temp = {"type": "Image", "path": img_path}
            chain.append(temp)
        request_data = {
            "sessionKey": self.session,
            "target": target,
            "messageChain": chain
        }
        url = self.url+'/sendGroupMessage'
        res = requests.post(url=url, json=request_data)

        try:
            json_data = res.json()
            if json_data['code'] != 0:
                print(f"消息发送失败: {json_data['code']}")
        except:
            print(f"链接异常: {res.text}")
        print(f"-> [{target}]: {msg}")

    def send_temp_message(self, target, QQ, msg: str, message_type="TEXT"):
        """
        向某群(target)中的某人(QQ)发起临时消息(msg)
        target: 群号
        QQ: 消息接收人的QQ
        msg: 发送的内容
        message_type: 消息类型（TEXT、IMG）
        """
        chain = []
        if message_type == "TEXT":
            temp = {"type": "Plain", "text": msg}
            chain.append(temp)
        elif message_type == "IMG":
            img_path = os.path.join(img_dir, msg)
            temp = {"type": "Image", "path": img_path}
            chain.append(temp)
        request_data = {
            "sessionKey": self.session,
            "qq": QQ,
            "group": target,
            "messageChain": chain
        }
        url = self.url + '/sendTempMessage'
        res = requests.post(url=url, json=request_data)

        try:
            json_data = res.json()
            if json_data['code'] != 0:
                print(f"消息发送失败: {json_data['code']}")
        except:
            print(f"链接异常: {res.text}")
        print(f"**-> [{target} - {QQ}]: {msg}")

    def get_group_member_list(self, target):
        """
        获取群成员列表
        target: 群号
        """
        request_data = {
            "sessionKey": self.session,
            "target": target
        }
        url = self.url + '/memberList'
        res = requests.post(url=url, json=request_data)

        try:
            json_data = res.json()
            if json_data['code'] != 0:
                print(f"获取群成员列表失败: {json_data['code']}")
            return json_data[0]
        except:
            print(f"链接异常: {res.text}")


qq = os.getenv("mirai_qq")
key = os.getenv("mirai_key")
mirai_ip = os.getenv("mirai_ip")
mirai_port = os.getenv("mirai_port")
mirai = Mirai(qq, key, mirai_ip, mirai_port)

if __name__ == "__main__":
    print(mirai.session)
    mirai.send_group_message(374664776, "hhhhh")
