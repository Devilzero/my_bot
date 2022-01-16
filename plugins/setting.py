import os

from utils.mirai_api import mirai
from utils.db_api import set_group_switch, get_group_switch
from utils.auth import get_permission_level, set_permission_level,\
    permission_level_dict as pl


group_switch_list = ["闭嘴", "说话"]
set_master_list = ["设置主人"]
menu_cmd = ["菜单", "功能", "你能干啥", "功能列表"]

cmd_head_list = [*group_switch_list, *set_master_list, *menu_cmd]

def mk_msg(data_json):
    from_qq = data_json['data']['sender']['id']
    form_group_id = data_json['data']['sender']['group']['id']
    from_msg = data_json['data']['messageChain'][1]['text']
    rev_list = from_msg.split()


    if rev_list[0] in group_switch_list:
        group_switch(from_qq, form_group_id, rev_list[0])

    elif rev_list[0] in set_master_list:
        set_master(from_qq, form_group_id, rev_list[1])
    elif rev_list[0] in menu_cmd:
        show_menu(form_group_id)


def show_menu(group_id):
    msg = """功能名称 | 相关命令

查询功能
  > 开服 / 开服 破阵子
  > 日常 / 日常 破阵子
  > 沙盘 / 沙盘 破阵子
  > 金价 / 金价 破阵子
  > 奇遇 黑白路
  > 更新公告
  > 宏 心法全称
情缘操作
  > 分配情缘 / 找情缘
  > 求情缘@QQ / 接受情缘@QQ
  > 情缘申请列表 / 我的情缘
  > 死情缘
发送黄图
  > 黄图
功能开关
  > 说话 / 闭嘴
"""
    mirai.send_group_message(group_id, msg)

def set_master(qq, group_id, master_qq):
    if str(qq) != os.getenv("founder"):
        return
    set_permission_level(int(master_qq), 100)
    mirai.send_group_message(group_id, f"好了，{master_qq}成为我的新主人了！", ATQQ=qq)

def group_switch(qq, group_id, action):
    switch = action=="说话"
    if get_group_switch(group_id) == switch:
        mirai.send_group_message(group_id, f"好的好的，在说了在说了。只要你说：“闭嘴”我就滚。")
        return
    if get_permission_level(qq, group_id) < pl["ADMINISTRATOR"]:
        if switch:
            mirai.send_group_message(group_id, f"不听不听，王八念经。老大不让我说话，谁找我都不好使！", ATQQ=qq)
        else:
            mirai.send_group_message(group_id, f"你算老几，让我闭嘴至少得群主说话才好使！", ATQQ=qq)
        return
    set_group_switch(group_id, switch)
    if switch:
        mirai.send_group_message(group_id, "我来了我来了！让我“闭嘴”我也会老老实实的闭嘴。")
    else:
        mirai.send_group_message(group_id, "那我就先闭嘴了，想让我继续说话的话那就跟我说句“说话”。\n而且我不会想你的，因为我只是个机器人。")
