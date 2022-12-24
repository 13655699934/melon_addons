#!/usr/local/bin/python
# -*-coding:utf-8-*-
# Desc: 短信http接口的python代码调用示例
# https://www.yunpian.com/api/demo.html
# https访问，需要安装  openssl-devel库。apt-get install openssl-devel

import http.client
import urllib
import json

# 服务地址
sms_host = "sms.yunpian.com"
# 短信语音服务地址
voice_host = "voice.yunpian.com"
# 端口号
port = 443
# 版本号
version = "v2"
# 查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
# 智能匹配模板短信接口的URI
sms_send_uri = "/" + version + "/sms/single_send.json"
# 模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_single_send.json"
# 语音短信接口的URI
sms_voice_send_uri = "/" + version + "/voice/send.json"
# 语音验证码
voiceCode = 1234


# def get_user_info(apikey):
#     """
#     取账户信息
#     """
#     conn = http.client.HTTPSConnection(sms_host, port=port)
#     headers = {
#         "Content-type": "application/x-www-form-urlencoded",
#         "Accept": "text/plain"
#     }
#     conn.request('POST', user_get_uri, urllib.parse.urlencode({'apikey': apikey}))
#     response = conn.getresponse()
#     response_str = response.read()
#     conn.close()
#     return response_str


def send_sms(apikey, text, mobile):
    """
    通用接口发短信
    """
    params = urllib.parse.urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    print ('response',response)
    response_str = response.read()
    conn.close()
    return response_str


def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.parse.urlencode({
        'apikey': apikey,
        'tpl_id': tpl_id,
        'tpl_value': urllib.parse.urlencode(tpl_value),
        'mobile': mobile
    })
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_voice_sms(apikey, code, mobile):
    """
    通用接口发短信
    """
    params = urllib.parse.urlencode({'apikey': apikey, 'code': code, 'mobile': mobile})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = http.client.HTTPSConnection(voice_host, port=port, timeout=30)
    conn.request("POST", sms_voice_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


if __name__ == '__main__':
    # 修改为您的apikey.可在官网（http://www.yunpian.com)登录后获取
    apikey = "b173139284df9373c79c6adbae43ffac"
    # 修改为您要发送的手机号码，多个号码用逗号隔开
    mobile = "13655699934"
    # 修改为您要发送的短信内容
    text = "【melon】有一条新的订单，请注意查收。"

    usertruename = "何双新"
    visitwebsite = "http://www.baidu.com"
    username = "melon"
    password = "123456"
    deadline = "2022-07-30"
    # 查账户信息
    # print(get_user_info(apikey))
    # 调用智能匹配模板接口发短信
    res=send_sms(apikey, text, mobile)
    print('res========',res)
    # 调用模板接口发短信
    tpl_id = 4825616  # 对应的模板内容为：您的验证码是#code#【#company#】
    tpl_value = {'#usertruename#': usertruename, '#visitwebsite#': visitwebsite, '#username#': username,
                 '#password#': password, '#deadline#': deadline}
    tpl_send_sms(apikey, tpl_id, tpl_value, mobile)
    # 调用模板接口发语音短信
    # print send_voice_sms(apikey,voiceCode,mobile)