from utils.mirai_api import mirai
import random

cmd_1 = ["黄图"]
find_qingyuan = ["找情缘", "帮我找情缘", "分配情缘"]

cmd_head_list = [*cmd_1, *find_qingyuan]


def mk_msg(data_json):
    form_group_id = data_json['data']['sender']['group']['id']
    from_msg = data_json['data']['messageChain'][1]['text']
    from_name = data_json['data']['sender']['memberName']
    rev_list = from_msg.split()

    if rev_list[0] in cmd_1:
        mirai.send_group_message(form_group_id, "emz/yellow.png", "IMG")
    elif rev_list[0] in cmd_head_list:
        group_member_list = mirai.get_group_member_list(form_group_id)
        usr = random.choice(group_member_list)
        msg_list = [
            f"【{from_name}】 跟 \n【{usr['memberName']}】 缘分到了，情个缘吧！",
            f"组织给【{from_name}】分配的情缘是\n【{usr['memberName']}】了，你们好好相处吧。",
            f"【{from_name}】跟\n【{usr['memberName']}】还挺有夫妻相，你俩私下聊聊吧。",
            f"祝【{from_name}】跟\n【{usr['memberName']}】永结同心！",
            f"祝【{from_name}】跟\n【{usr['memberName']}】早生贵子！",
            f"组织给【{from_name}】分配了情缘\n【{usr['memberName']}】",
            f"【{from_name}】跟\n【{usr['memberName']}】情缘了，不能反悔，谁反悔谁是小狗",
        ]
        msg = random.choice(msg_list)
        mirai.send_group_message(form_group_id, msg, "TXT")

