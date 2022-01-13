from utils.mirai_api import mirai
import random

cmd_1 = ["黄图"]
find_qingyuan = ["找情缘", "帮我找情缘", "分配情缘"]

cmd_head_list = [*cmd_1, *find_qingyuan]


def mk_msg(rev_list, group_id, qq, name):
    if rev_list[0] in cmd_1:
        return "emz/yellow.png", "IMG"
    elif rev_list[0] in cmd_head_list:
        group_member_list = mirai.get_group_member_list(group_id)
        usr = random.choice(group_member_list)
        msg_list = [
            f"【{name}】 跟 \n【{usr['memberName']}】 缘分到了，情个缘吧！",
            f"组织给【{name}】分配的情缘是\n【{usr['memberName']}】了，你们好好相处吧。",
            f"【{name}】跟\n【{usr['memberName']}】还挺有夫妻相，你俩私下聊聊吧。",
            f"祝【{name}】跟\n【{usr['memberName']}】永结同心！",
            f"祝【{name}】跟\n【{usr['memberName']}】早生贵子！",
            f"组织给【{name}】分配了情缘\n【{usr['memberName']}】",
            f"【{name}】跟\n【{usr['memberName']}】情缘了，不能反悔，谁反悔谁是小狗",
        ]
        return random.choice(msg_list)

