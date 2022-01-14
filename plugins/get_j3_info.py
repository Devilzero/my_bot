import os
import requests

from pymongo import MongoClient
from utils.mirai_api import mirai
from utils.auth import get_permission_level, \
    permission_level_dict as pl

mg_ip = os.getenv("mongdb_ip")
mg_port = os.getenv("mongodb_port")
mg_usr = os.getenv("mongodb_username")
mg_pwd = os.getenv("mongodb_password")


base_url = "https://www.jx3api.com/app/"

def get_server(group_id):
    client = MongoClient(f'mongodb://{mg_ip}:{mg_port}/', username=mg_usr, password=mg_pwd)
    with client:
        db = client.my_bot
        group_conf = db.group_conf.find_one({"_id": group_id})
        if not(group_conf and group_conf.get("server")):
            return False
        return group_conf.get("server")

def get_j3_info(api, data):
    url = base_url + api
    req = requests.post(url=url, data=data)
    if req.status_code == 200:
        return req.json()

def bind_server(qq, group_id, server):
    if get_permission_level(qq, group_id) < pl["ADMINISTRATOR"]:
        mirai.send_group_message(group_id, "权限不足，叫你们老大出来，这个玩意至少要管理员才能改！", ATQQ=qq)
        return
    client = MongoClient(f'mongodb://{mg_ip}:{mg_port}/', username=mg_usr, password=mg_pwd)
    with client:
        db = client.my_bot
        db.group_conf.update_one({'_id': group_id}, {'$set': {"server": server}}, True)
    mirai.send_group_message(group_id, "修改完成！")


def get_daily(group_id, server=""):
    if not server:
        server = get_server(group_id)
    if not server:
        mirai.send_group_message(group_id, "请绑定区服\n例如：\n绑定区服 破阵子\n\n或是输入要查询的区服\n例如：日常 破阵子")
        return
    data = {
        "server": server
    }
    req_json = get_j3_info("daily", data)
    msgInfo = """
阵营：{dayCamp}
战场：{dayBattle}
驰援：{dayPublic}
大战：{dayWar}
周常：{weekFive}
十人：{weekTeam}
公共：{weekPublic}""".format_map(req_json["data"])

    mirai.send_group_message(group_id, msgInfo)

def get_check(group_id, server=""):
    if not server:
        server = get_server(group_id)
    if not server:
        mirai.send_group_message(group_id, "请绑定区服\n例如：\n绑定区服 破阵子\n\n或是输入要查询的区服\n例如：日常 破阵子")
        return
    data = {
        "server": server,
    }
    req_json = get_j3_info("check", data)
    print(req_json)
    check_code = req_json["data"]["status"]
    if check_code == 1:
        msgInfo = f"【{server}】开服了！"
    else:
        msgInfo = f"【{server}】还没开服"

    mirai.send_group_message(group_id, msgInfo)

def get_macro(group_id, xinfa):
    data = {
        "name": xinfa
    }
    req_json = get_j3_info("macro", data)
    msgInfo = """
>> {name} <<

{macro}

{qixue}

更新时间：{time}
""".format_map(req_json['data'])
    mirai.send_group_message(group_id, msgInfo)

daily_head_list = ["日常"]
bind_head_list = ["绑定区服", "设置区服", "修改区服"]
check_head_list = ["开服"]
macro_head_list = ["宏"]

cmd_head_list = [*daily_head_list, *bind_head_list, *check_head_list, *macro_head_list]

def mk_msg(data_json):
    from_qq = data_json['data']['sender']['id']
    form_group_id = data_json['data']['sender']['group']['id']
    from_msg = data_json['data']['messageChain'][1]['text']
    rev_list = from_msg.split()

    if rev_list[0] in daily_head_list:
        if len(rev_list) < 2:
            server = ""
        else:
            server = rev_list[1]
        get_daily(form_group_id, server)

    if rev_list[0] in bind_head_list:
        if len(rev_list) < 2:
            mirai.send_group_message(form_group_id, "请输入区服\n例如：绑定区服 破阵子")
        else:
            server = rev_list[1]
            bind_server(from_qq, form_group_id, server)

    if rev_list[0] in check_head_list:
        get_check(form_group_id)

    if rev_list[0] in macro_head_list:
        xinfa = rev_list[1]
        get_macro(form_group_id, xinfa)