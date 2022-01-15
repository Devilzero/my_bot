from utils.mirai_api import mirai
from utils.db_api import update_shafttime_axis, get_shafttime_axis, get_user_info, update_user_info
import random
import datetime

cmd_1 = ["黄图"]
find_partner = ["找情缘", "帮我找情缘", "分配情缘"]
qiu_partner = ["求情缘"]
jieshou_partner = ["接受", "接受情缘"]
partner_req_list = ["情缘申请列表", "我的鱼塘"]
fuck_partner_list = ["死情缘"]
my_partner_list = ["我的情缘", "遛情缘"]

cmd_head_list = [*cmd_1, *find_partner, *qiu_partner, *jieshou_partner, *partner_req_list, *fuck_partner_list, *my_partner_list]


def mk_msg(data_json):
    form_group_id = data_json['data']['sender']['group']['id']
    from_msg = data_json['data']['messageChain'][1]['text']
    from_name = data_json['data']['sender']['memberName']
    from_qq = data_json['data']['sender']['id']
    rev_list = from_msg.split()

    if rev_list[0] in cmd_1:
        mirai.send_group_message(form_group_id, "emz/yellow.png", "IMG")

    elif rev_list[0] in find_partner:
        find_partner_time = get_shafttime_axis(from_qq, "find_partner_time")
        if find_partner_time:
            wait_time = (datetime.datetime.now() - find_partner_time).total_seconds()
            if wait_time < 180:
                r_s = 3600 - wait_time
                mirai.send_group_message(form_group_id, f"一小时只能找一次情缘！{int(r_s/60)} 分钟后再来吧！", "TXT", ATQQ=from_qq)
                return

        cur_time =  datetime.datetime.now()
        update_shafttime_axis(from_qq, {"find_partner_time": cur_time})
        group_member_list = mirai.get_group_member_info(form_group_id)
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
        mirai.send_group_message(form_group_id, msg, "TXT", ATQQ=usr["id"])
    elif rev_list[0] in qiu_partner:
        at_list = []
        for i in data_json['data']['messageChain']:
            if i["type"] == "At":
                at_list.append(i["target"])
        if len(at_list) < 1:
            mirai.send_group_message(form_group_id, "连人都不@，我去哪给你牵线？要求情缘记得@对方！", "TXT", ATQQ=from_qq)
            return
        elif len(at_list) > 1:
            mirai.send_group_message(form_group_id, "你还想找几个情缘？全群都当你情缘得了呗", "TXT", ATQQ=from_qq)
            return
        target_qq = at_list[0]
        if target_qq == from_qq:
            mirai.send_group_message(form_group_id, f"大家快来看啊！【{from_name}】要跟自己情缘了！", "TXT")
            return

        # 是否重复申请
        partner_wait_list = get_shafttime_axis(target_qq, "partner_wait")
        if partner_wait_list:
            for i in partner_wait_list:
                if str(i["qq"]) == str(from_qq):
                    mirai.send_group_message(form_group_id, "你都跟这位同学求过一次情缘了。成就成，不成就不成，这事强求不来。", "TXT")
                    return

        # 查询双方是否已有情缘
        partner_info = get_user_info(from_qq, "partner")
        if partner_info:
            mirai.send_group_message(form_group_id, f"赶紧管管【{from_name}】，都有情缘了还来求情缘？", "TXT", ATQQ=partner_info["qq"])
            return
        target_partner_info = get_user_info(target_qq, "partner")
        if target_partner_info:
            mirai.send_group_message(form_group_id, f"对方有情缘了，强扭的瓜不甜，换个人吧！", "TXT", ATQQ=from_qq)
            return

        # 查询等待时间
        partner_time = get_shafttime_axis(from_qq, "partner_time")
        if partner_time:
            wait_time = (datetime.datetime.now() - partner_time).total_seconds()
            if wait_time < 180:
                r_s = 180 - wait_time
                mirai.send_group_message(form_group_id, f"3分钟只能求一次情缘！{int(r_s)} 秒后再来吧！", "TXT", ATQQ=from_qq)
                return
        # 正式求情缘
        mirai.send_group_message(form_group_id, f"【{from_name}】向你求情缘了，如果回复“接受情缘”并@{from_name}，你们就可以绑定情缘了！", "TXT", ATQQ=target_qq)
        cur_time =  datetime.datetime.now()
        update_shafttime_axis(from_qq, {"partner_time": cur_time})
        # 加入请求列表
        target_wait_list = get_shafttime_axis(target_qq, "partner_wait")
        if target_wait_list:
            target_wait_list.append({"date_time": cur_time, "qq": from_qq, "name": from_name})
        else:
            target_wait_list = [{"date_time": cur_time, "qq": from_qq, "name": from_name}]
        update_shafttime_axis(target_qq, {"partner_wait": target_wait_list})

    elif rev_list[0] in jieshou_partner:
        partner_wait_list = get_shafttime_axis(from_qq, "partner_wait")
        if not partner_wait_list:
            mirai.send_group_message(form_group_id, "没有人跟你求情缘！", "TXT", ATQQ=from_qq)
            return
        at_list = rev_list[1:]
        for i in data_json['data']['messageChain']:
            if i["type"] == "At":
                at_list.append(i["target"])
        if len(at_list) < 1:
            mirai.send_group_message(form_group_id, "想接受谁的情缘就直接@对方吧！或者写上qq号也行！", "TXT", ATQQ=from_qq)
            return
        elif len(at_list) > 1:
            mirai.send_group_message(form_group_id, "你只能同意一个申请！", "TXT", ATQQ=from_qq)
            return
        target_qq = at_list[0]

        for i in partner_wait_list:
            if str(target_qq) == str(i.get("qq")):
                cur_time =  datetime.datetime.now()
                update_user_info(target_qq, {"partner": {"qq": from_qq, "date_time": cur_time, "name": from_name}})
                update_user_info(from_qq, {"partner": {"qq": target_qq, "date_time": cur_time, "name": i['name']}})
                mirai.send_group_message(form_group_id, f"【{from_name}】【{i['name']}】正式结为情缘！祝二位永结同心！", "TXT")
                update_shafttime_axis(target_qq, {"partner_wait": []})
                update_shafttime_axis(from_qq, {"partner_wait": []})
                return
        mirai.send_group_message(form_group_id, "对方根本没跟你求情缘！可以通过“情缘申请列表”查看谁向你求情缘了！", "TXT", ATQQ=from_qq)
    elif rev_list[0] in partner_req_list:
        partner_wait_list = get_shafttime_axis(from_qq, "partner_wait")
        if not partner_wait_list:
            mirai.send_group_message(form_group_id, "没有人跟你求情缘！", "TXT", ATQQ=from_qq)
            return
        msg = f"【{from_name}】的{rev_list[0]}\n"
        msg += "\n".join([f"{i['name']}({i['qq']}) {i['date_time'].strftime('%Y-%m-%d %H:%M:%S')}" for i in partner_wait_list])
        mirai.send_group_message(form_group_id, msg, "TXT", ATQQ=from_qq)

    elif rev_list[0] in fuck_partner_list:
        partner_info = get_user_info(from_qq, "partner")
        if not partner_info:
            mirai.send_group_message(form_group_id, "你根本就没有情缘！", "TXT", ATQQ=from_qq)
            return
        update_user_info(partner_info["qq"], {"partner": None})
        update_user_info(from_qq, {"partner": None})
        mirai.send_group_message(form_group_id, f"【{from_name}】跟你死了情缘。\n江湖路远，各自珍重。", "TXT", ATQQ=partner_info["qq"])

    elif rev_list[0] in my_partner_list:
        partner_info = get_user_info(from_qq, "partner")
        if not partner_info:
            mirai.send_group_message(form_group_id, "你还没有情缘！", "TXT", ATQQ=from_qq)
            return
        msg = f"【{from_name}】的情缘是【{partner_info['name']}】。\n{partner_info['date_time'].strftime('%Y-%m-%d %H:%M:%S')} 正式结为情缘"
        mirai.send_group_message(form_group_id, msg, "TXT", ATQQ=partner_info["qq"])
