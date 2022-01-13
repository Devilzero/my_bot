cmd_1 = ["黄图"]

cmd_head_list = [*cmd_1]


def mk_msg(rev_list, group_id, qq):
    if rev_list[0] in cmd_1:
        return "emz/yellow.png", "IMG"
