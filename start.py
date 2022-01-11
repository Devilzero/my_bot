# -*- coding: utf-8 -*-
import os
import json

with open("conf/config.json", "r") as f:
    config = json.load(f)
os.environ.update(config)

from http.server import HTTPServer, BaseHTTPRequestHandler
import requests as request
from urllib import parse
from get_j3_info import mk_msg



myqq_token = os.getenv("myqq_token")
myqq_http_ip = os.getenv("myqq_http_ip")
myqq_http_port = os.getenv("myqq_http_port")
j3bot_ip = os.getenv("j3bot_ip")
j3bot_port = os.getenv("j3bot_port")

# 字典类型数据None数据处理功能
def dict_clean(items):
    result = {}
    for key, value in items:
        if value is None:
            value = '没有找到'
        result[key] = value
    return result


# 全角->半角转换功能
def strQ2B(ustring):
    ss = ''
    for s in ustring:
        restring = ''
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            restring += chr(inside_code)
        ss += restring
    return ss



# 发送消息处理方法
def apiSendMsg(raw_rev):

    try:
        # 本示例以GET为例，官方主推POST
        # 相关参数说明
        """
            参数一：调用URL含接口
            参数二：接口调用所需参数，该参数以JSON形式返回
            参数三：是否需要验证
        """
        apiUrl = f"http://{myqq_http_ip}:{myqq_http_port}/MyQQHTTPAPI?"
        recMsg = parse.unquote(raw_rev['MQ_msg'])
        # 消息全半角处理
        params = {
            'function': 'Api_SendMsg',
            # 记得修改成自己的
            'token': myqq_token,
            'c1': raw_rev['MQ_robot'],
            'c2': raw_rev['MQ_type'],
        }
        if raw_rev['MQ_type'] == 2:
            params.update({
                "c3": raw_rev['MQ_fromID']
            })
        elif raw_rev['MQ_type'] == 1:
            params.update({
                "c4": raw_rev['MQ_fromQQ']
            })
        recMsg = strQ2B(recMsg)
        func, msgInfo = mk_msg(recMsg, raw_rev.get("MQ_fromID"))
        if msgInfo:
            # 如果为菜单指令时添加C5为菜单变量值
            params.update({'function': func})
            if func == "Api_SendMsg":
                params.update({'c5': msgInfo})
            elif func == "Api_UpLoadPic":
                params.update({'c4': msgInfo})
            # GET后获取结果集
            print(params)
            result = request.get(apiUrl, params=params, verify=False)

            # 返回处理结果集
            return result
    except Exception as e:
        print('error:', e)


# @Time : 2021-09-10 9:22
# @Author : Kwoky
# @Version：V 1.0
# @File : DaenQQ.py
# @Desc : 消息回显处理
class DaenQQ(BaseHTTPRequestHandler):

    # 调用接口统一处理功能
    # 根据个人情况可单独封装方法便于调用
    # 本例中仅以消息回调触发条件后执行相应操作为例
    # 回调消息获取后业务逻辑处理(根据个人情况，按个人需求处理即可)
    def do_POST(self):
        '''
            转换为字典类型后读取回调消息(以下为官方API接口返回json详解)
            MQ_robot	用于判定哪个QQ接收到该消息
            MQ_type	接收到消息类型，该类型可在[常量列表]中查询具体定义
            MQ_type_sub	此参数在不同情况下，有不同的定义
            MQ_fromID	此消息的来源，如：群号、讨论组ID、临时会话QQ、好友QQ等
            MQ_fromQQ	主动发送这条消息的QQ，踢人时为踢人管理员QQ
            MQ_passiveQQ	被动触发的QQ，如某人被踢出群，则此参数为被踢出人QQ
            MQ_msg	（此参数将被URL UTF8编码，您收到后需要解码处理）此参数有多重含义，常见为：对方发送的消息内容，但当消息类型为 某人申请入群，则为入群申请理由,当消息类型为收到财付通转账、收到群聊红包、收到私聊红包时为原始json，详情见[特殊消息]章节
            MQ_msgSeq	撤回别人或者机器人自己发的消息时需要用到
            MQ_msgID	撤回别人或者机器人自己发的消息时需要用到
            MQ_msgData	UDP收到的原始信息，特殊情况下会返回JSON结构（入群事件时，这里为该事件data）
            MQ_timestamp	对方发送该消息的时间戳，引用回复消息时需要用到
        '''
        # 回调消息获取
        raw_rev_data = self.rfile.read(int(self.headers['content-length'])).decode()
        raw_rev = json.loads(raw_rev_data)

        # 触发条件后根据实际情况处理调用情况
        apiSendMsg(raw_rev)


# 程序执行入口
if __name__ == '__main__':

    # 第一参数为回调地址，第二参数为回调接口
    host = (j3bot_ip, int(j3bot_port))
    # 调用HTTP服务器
    server = HTTPServer(host, DaenQQ)
    # 服务启动控制台提醒
    print(f"Starting server, listen at: {j3bot_ip}:{j3bot_port}")
    # 服务启动挂载(保持服务一直在线)
    server.serve_forever()
