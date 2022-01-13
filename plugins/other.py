from utils.mirai_api import mirai
import random

cmd_1 = ["黄图"]
find_qingyuan = ["找情缘", "帮我找情缘"]

cmd_head_list = [*cmd_1, *find_qingyuan]


def mk_msg(rev_list, group_id, qq, name):
    if rev_list[0] in cmd_1:
        return "emz/yellow.png", "IMG"
    elif rev_list[0] in cmd_head_list:
        group_member_list = mirai.get_group_member_list(group_id)
        usr = random.choice(group_member_list)
        msg = f"{name}({qq}) 跟 {usr['memberName']}({usr['id']}) 缘分到了，情个缘吧！"
        return msg

