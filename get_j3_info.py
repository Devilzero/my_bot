import os
import time
import requests

from pymongo import MongoClient

mg_ip = os.getenv("mongdb_ip")
mg_port = os.getenv("mongodb_port")
mg_usr = os.getenv("mongodb_username")
mg_pwd = os.getenv("mongodb_password")


base_url = "https://www.jx3api.com/app/"

def get_server(group_id):
    client = MongoClient(f'mongodb://{mg_ip}:{mg_port}/', username=mg_usr, password=mg_pwd)
    with client:
        db = client.group
        config = db.config.find_one({"_id": group_id})
        if not(config and config.get("server")):
            return False
        return config.get("server")

def get_j3_info(api, data):
    url = base_url + api

    req = requests.post(url=url, data=data)
    if req.status_code == 200:
        return req.json()

def bind_server(group_id, server):
    client = MongoClient(f'mongodb://{mg_ip}:{mg_port}/', username=mg_usr, password=mg_pwd)
    with client:
        db = client.group
        db.config.update_one({'_id': group_id}, {'$set': {"server": server}}, True)
    return "Api_SendMsg", "修改完成！"


def get_daily(group_id, server=""):
    if not server:
        server = get_server(group_id)
    if not server:
        return "Api_SendMsg", "请绑定区服\n例如：\n绑定区服 破阵子\n\n或是输入要查询的区服\n例如：日常 破阵子"
    data = {
        "server": server
    }
    req_json = get_j3_info("daily", data)
    print(req_json)
    msgInfo = """
阵营：{dayCamp}
战场：{dayBattle}
驰援：{dayPublic}
大战：{dayWar}
周常：{weekFive}
十人：{weekTeam}
公共：{weekPublic}""".format_map(req_json["data"])

    return "Api_SendMsg", msgInfo

def get_check(group_id, server=""):
    if not server:
        server = get_server(group_id)
    if not server:
        return "Api_SendMsg", "请绑定区服\n例如：\n绑定区服 破阵子\n\n或是输入要查询的区服\n例如：日常 破阵子"
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

    return "Api_SendMsg", msgInfo

def get_macro(name):
    data = {
        "name": name
    }
    req_json = get_j3_info("macro", data)
    msgInfo = """
>> {name} <<

{macro}

{qixue}

更新时间：{time}
""".format_map(req_json['data'])
    return "Api_SendMsg", msgInfo

def mk_msg(recMsg, group_id):
    rev_list = recMsg.split("+")
        # 触发菜单指令

    if rev_list[0] == '日常':
        if len(rev_list) < 2:
            server = ""
        else:
            server = rev_list[1]
        return get_daily(group_id, server)

    if rev_list[0] in ["绑定区服", "设置区服", "修改区服"]:
        if len(rev_list) < 2:
            return "请输入区服\n例如：绑定区服 破阵子"
        else:
            server = rev_list[1]
            return bind_server(group_id, server)

    if rev_list[0] in ["开服"]:
        return get_check(group_id)

    if rev_list[0] in ["宏"]:
        name = rev_list[1]
        return get_macro(name)