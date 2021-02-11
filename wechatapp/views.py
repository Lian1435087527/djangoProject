from django.shortcuts import render

# Create your views here.
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse
from wechatpy import WeChatClient, parse_message, create_reply
import json

# 这里的token 取自微信公众号自己设置的
token = 'fan'
a = 0


def handle_wx(request):
    # GET 方式用于微信公众平台绑定验证
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = '错误的请求'
        response = HttpResponse(echo_str)
        return response
    else:
        msg = parse_message(request.body)
        print(msg)
        client = WeChatClient(
            "wx7d69afbab1a0647d",
            "8026876b1390670f3dca1f8f8e3ddc6f")
        # print(msg.id,msg.source,msg.target,msg.create_time,msg.type)
        # print(request.body)
        global a
        ret_mothod_dic = {"event": "Text_ret"}
        if msg.type == "event":
            print(msg.event)
            if msg.event == "click":
                str_rsp = create_reply("12321521"+"<a href=\"https://s3.ax1x.com/2021/02/03/ylKwc9.png\">显示文字</a>"+"  d faf21521", msg)
            elif msg.event == "view":
                str_rsp = create_reply(str("a"), msg)
            else:
                str_rsp = create_reply(str("C"), msg)
        elif msg.type == "text":
            str_rsp = Text_ret(msg)
        elif msg.type == "voice":
            str_rsp = create_reply("欢迎来到李师傅修改衣裤裙店\n请点击按钮使用相关功能", msg)
        else:
            str_rsp = create_reply("欢迎关注李师傅修改衣裤裙店，二十年老字号。\n给我一个机会，让您穿出舒服、苗条、美丽。", msg)
        # client.menu.delete()
        # client.menu.try_match(msg.id)
        # jsondict=json.load(client.menu.get())

        # articles_reply = create_reply(str_rsp, message=msg)
        # print(client.material.batchget("news"))
        # print(
        #     client.menu.try_match(
        #         msg.source), '\n', type(
        #         client.menu.get()["conditionalmenu"][0]))
        a += 1
        response = HttpResponse(
            str_rsp.render(),
            content_type='application/xml')
        return response


def Text_ret(msg):
    str_rsp = create_reply([
        {
            'title': 'test',
            'description': 'test',
            'image': 'https://s2.doyo.cn/img/5b/3e/d2ef9e9e78695d00000e.jpg',
            'url': 'https://m.doyo.cn/article/360047'
        },
        # add more ...
    ], msg)
    return str_rsp


def create_menu(request):
    # 第一个参数是公众号里面的appID，第二个参数是appsecret
    # 老妈的
    # client = WeChatClient("wx2abf89713b9ec1ce", "7af55f1b8557c382e9507bb106204f57")
    # 测试的
    client = WeChatClient(
        "wx7d69afbab1a0647d",
        "8026876b1390670f3dca1f8f8e3ddc6f")
    client.menu.del_conditional(
        client.menu.get()["conditionalmenu"][0]["menuid"])
    client.menu.add_conditional({
        "button": [
            {
                "type": "view",
                "name": "歌曲44",
                "url": "https://router.map.qq.com/short?l=c94ba04ec32777ae43959c56b7c46e5e"
            },
            {
                "type": "click",
                "name": "歌手77",
                "key": "V1001_TODAINGER"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "https://mp.weixin.qq.com/s/xvFRKfLr_83H_5K7qZfBgQ"
                    },
                    {
                        "type": "view",
                        "name": "视频",
                        "url": "http://v.qq.com/"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }
                ]
            }
        ],
        "matchrule": {
            # "group_id": "2",
            "sex": "2",
            "country": "中国",
            # "province": "广东",
            # "city": "广州",
            "client_platform_type": "2"
        }
    })

    # print(client.menu.get_menu_info(),'\n')
    print(client.menu.get())
    # client.menu.delete()
    # print(client.menu.get_menu_info(), '\n', client.menu.get())
    return HttpResponse('ok')
