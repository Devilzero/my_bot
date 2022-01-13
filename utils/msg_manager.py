import os
import sys
import json
from utils.mirai_api import mirai

plugins_dir = os.path.realpath(__file__+"/../../plugins/")
sys.path.append(os.path.realpath(__file__+"/../../plugins/"))


def dispatch_msg(msg, group_id="", qq="", name=""):
    rev_list = msg.split()
    for i in os.listdir(plugins_dir):
        if i.endswith(".py"):
            plugin_name = i.split(".")[0]
            plugin = __import__(f"{plugin_name}")
            if rev_list[0] in plugin.cmd_head_list:
                return plugin.mk_msg(rev_list, group_id, qq, name)


def msg_manager(message):
    data_json = json.loads(message)
    if data_json['data']['type'] == 'GroupMessage':
        # 群聊
        if data_json['data']['messageChain'][1]['type'] == 'Plain':
            from_qq = data_json['data']['sender']['id']
            from_name = data_json['data']['sender']['memberName']
            form_group_id = data_json['data']['sender']['group']['id']
            from_group_name =data_json['data']['sender']['group']['name']
            from_msg = data_json['data']['messageChain'][1]['text']
            print(f"<- {from_group_name}({form_group_id}) - {from_name}({from_qq}): {from_msg}")
            from_msg = dispatch_msg(from_msg, form_group_id, from_qq, from_name)
            message_type = "TEXT"
            if from_msg:
                if isinstance(from_msg, str) == 1:
                    msg = from_msg
                elif isinstance(from_msg, tuple):
                    msg, message_type = from_msg
                mirai.send_group_message(form_group_id, msg, message_type)
    elif data_json['data']['type'] == 'FriendMessage':
        # 好友
        if data_json['data']['messageChain'][1]['type'] == 'Plain':
            from_qq = data_json['data']['sender']['id']
            from_nickname = data_json['data']['sender']['nickname']
            from_remark = data_json['data']['sender'].get('remark')
            from_msg = data_json['data']['messageChain'][1]['text']
            from_name = from_remark if from_remark else from_nickname
            print(f"<- {from_name}({from_qq}): {from_msg}")
    elif data_json['data']['type'] == 'TempMessage':
        # 临时
        if data_json['data']['messageChain'][1]['type'] == 'Plain':
            from_qq = data_json['data']['sender']['id']
            from_name = data_json['data']['sender']['memberName']
            form_group_id = data_json['data']['sender']['group']['id']
            from_group_name =data_json['data']['sender']['group']['name']
            from_msg = data_json['data']['messageChain'][1]['text']
            print(f"<-** {from_group_name}({form_group_id}) - {from_name}({from_qq}): {from_msg}")
            mirai.send_temp_message(form_group_id, from_qq, "噶哈？")