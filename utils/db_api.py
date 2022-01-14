import os
import sys

sys.path.append(os.path.realpath(__file__ + "/../.."))
from utils.log import log
from pymongo import MongoClient

mg_ip = os.getenv("mongdb_ip")
mg_port = os.getenv("mongodb_port")
mg_usr = os.getenv("mongodb_username")
mg_pwd = os.getenv("mongodb_password")


def create_client():
    """
    创建mongodb客户端
    """
    return MongoClient(f'mongodb://{mg_ip}:{mg_port}/', username=mg_usr, password=mg_pwd)


def get_group_conf(group_id, item=""):
    """
    获取群配置
    """
    client = create_client()
    with client:
        db = client.my_bot
        group_conf = db.group_conf.find_one({'_id': group_id})
    if item:
        return group_conf.get(item)
    return group_conf

def update_group_conf(group_id, data):
    """
    更新群配置
    """
    client = create_client()
    with client:
        db = client.my_bot
        db.group_conf.update_one({'_id': group_id}, {'$set':data}, True)

def set_group_switch(group_id, switch):
    """
    修改群开关
    """
    client = create_client()
    with client:
        db = client.my_bot
        db.group_conf.update_one({'_id': group_id}, {'$set': {"group_switch": switch}}, True)

def get_group_switch(group_id):
    """
    查看群开关
    """
    switch = get_group_conf(group_id, "group_switch")
    return switch


def get_user_info(qq):
    """
    获取用户信息
    """
    client = create_client()
    with client:
        db = client.my_bot
        return db.user_info.find_one({"_id": qq})

def update_user_info(qq, data):
    """
    更新用户信息
    """
    client = create_client()
    with client:
        db = client.my_bot
        db.user_info.update_one({'_id': qq}, {'$set':data}, True)



if __name__ == "__main__":
    print(get_group_switch(129903168))