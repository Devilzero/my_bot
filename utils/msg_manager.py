import os
import sys
import json
import time
from utils.mirai_api import mirai
from utils.log import log
from utils.db_api import set_group_switch
from utils.db_api import get_group_switch

plugins_dir = os.path.realpath(__file__+"/../../plugins/")
sys.path.append(os.path.realpath(__file__+"/../../plugins/"))


exception_list = ["说话", "设置主人"]

# def dispatch_msg(msg, group_id="", qq="", name=""):
def dispatch_msg(data_json, form_group_id):
    msg = data_json['data']['messageChain'][1]['text']
    rev_list = msg.split()
    for i in os.listdir(plugins_dir):
        if i.endswith(".py"):
            plugin_name = i.split(".")[0]
            plugin = __import__(f"{plugin_name}")
            if rev_list[0] in plugin.cmd_head_list:
                if rev_list[0] in exception_list or get_group_switch(form_group_id):
                    return plugin.mk_msg(data_json)


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
            log.write_log(f"<- {from_group_name}({form_group_id}) - {from_name}({from_qq}): {from_msg}", form_group_id)
            dispatch_msg(data_json, form_group_id)
    elif data_json['data']['type'] == 'FriendMessage':
        # 好友
        if data_json['data']['messageChain'][1]['type'] == 'Plain':
            from_qq = data_json['data']['sender']['id']
            from_nickname = data_json['data']['sender']['nickname']
            from_remark = data_json['data']['sender'].get('remark')
            from_msg = data_json['data']['messageChain'][1]['text']
            from_name = from_remark if from_remark else from_nickname
            log.info(f"<- {from_name}({from_qq}): {from_msg}")
    elif data_json['data']['type'] == 'TempMessage':
        # 临时
        if data_json['data']['messageChain'][1]['type'] == 'Plain':
            from_qq = data_json['data']['sender']['id']
            from_name = data_json['data']['sender']['memberName']
            form_group_id = data_json['data']['sender']['group']['id']
            from_group_name =data_json['data']['sender']['group']['name']
            from_msg = data_json['data']['messageChain'][1]['text']
            log.info(f"<-** {from_group_name}({form_group_id}) - {from_name}({from_qq}): {from_msg}")
            mirai.send_temp_message(form_group_id, from_qq, "噶哈？")
    elif data_json['data']['type'] == 'BotInvitedJoinGroupRequestEvent':
        event_id = data_json['data']["eventId"]
        from_id = data_json['data']["fromId"]
        group_id = data_json['data']["groupId"]
        nick = data_json['data']["nick"]
        group_name = data_json['data']["groupName"]
        log.info(f"+-> {nick}({from_id}) 邀请我进群: {group_name}({group_id})")
        mirai.processing_of_group_applications(event_id, from_id, group_id, 0)
        set_group_switch(group_id, True)
        time.sleep(3)
        msg = "大家好！我是二猫子，是个努力干活还不粘人的机器人。\n发送“菜单”就可以查看我能干啥了。\n如果不想让我说话，可以让管理员跟我说“闭嘴”，这样我就会麻溜的滚蛋了。"
        mirai.send_group_message(group_id, msg)