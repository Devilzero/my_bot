import os

from pymongo import MongoClient

from utils import constant as con
from utils.mirai_api import mirai


mg_ip = os.getenv("mongdb_ip")
mg_port = os.getenv("mongodb_port")
mg_usr = os.getenv("mongodb_username")
mg_pwd = os.getenv("mongodb_password")


con.MASTER = 100       # 主人
con.SUPER_ADMIN = 5    # 超级管理员
con.OWNER = 2          # 群主
con.ADMINISTRATOR = 1  # 群管理员
con.MEMBER = 0         # 群成员
con.BLACK_USER = -1    # 黑名单用户

permission_level_dict = {
    "MASTER": con.MASTER,
    "SUPER_ADMIN": con.SUPER_ADMIN,
    "OWNER": con.OWNER,
    "ADMINISTRATOR": con.ADMINISTRATOR,
    "MEMBER": con.MEMBER,
    "BLACK_USER": con.BLACK_USER
}


def get_permission_level(qq, group_id=None):
    permission_level = con.MEMBER
    client = MongoClient(
        f'mongodb://{mg_ip}:{mg_port}/', username=mg_usr, password=mg_pwd)
    with client:
        db = client.my_bot
        user_info = db.user_info.find_one({"_id": qq})
        if user_info:
            permission_level = user_info.get("permission_level", con.MEMBER)
    if permission_level <= con.MEMBER and group_id:
        member_info = mirai.get_group_member_info(group_id, qq)
        if member_info:
            permission_level = permission_level_dict.get(
                member_info.get("permission"), con.MEMBER)
    return permission_level


def set_permission_level(qq, permission_level=0):
    client = MongoClient(
        f'mongodb://{mg_ip}:{mg_port}/', username=mg_usr, password=mg_pwd)
    with client:
        db = client.my_bot
        db.user_info.update_one(
            {'_id': qq}, {'$set': {"permission_level": permission_level}}, True)
