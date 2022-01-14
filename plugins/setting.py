import os

from utils.mirai_api import mirai
from utils.db_api import set_group_switch, get_group_switch
from utils.auth import get_permission_level, \
    permission_level_dict as pl


group_switch_list = ["闭嘴", "说话"]

cmd_head_list = [*group_switch_list]

def mk_msg(data_json):
    from_qq = data_json['data']['sender']['id']
    form_group_id = data_json['data']['sender']['group']['id']
    from_msg = data_json['data']['messageChain'][1]['text']
    rev_list = from_msg.split()


    if rev_list[0] in group_switch_list:
        group_switch(from_qq, form_group_id, rev_list[0])


def group_switch(qq, group_id, action):
    switch = action=="说话"
    if get_group_switch(group_id) == switch:
        return
    if get_permission_level(qq, group_id) < pl["OWNER"]:
        if switch:
            mirai.send_group_message(group_id, f"不听不听，王八念经。老大不让我说话，谁找我都不好使！", ATQQ=qq)
        else:
            mirai.send_group_message(group_id, f"你算老几，让我闭嘴至少得群主说话才好使！", ATQQ=qq)
        return
    set_group_switch(group_id, switch)
    if switch:
        mirai.send_group_message(group_id, "我来了我来了！")
    else:
        mirai.send_group_message(group_id, "那我就先闭嘴了，想让我继续说话的话那就跟我说句说话。\n而且我不会想你的，因为我只是个机器人。")
