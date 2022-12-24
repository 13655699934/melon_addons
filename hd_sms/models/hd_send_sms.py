# -*- coding: utf-8 -*-
import http.client
import urllib
import json
from odoo import api, fields, models, _
import datetime


class HdSendSms(models.Model):
    _name = "hd.send.sms"
    _description = "发送短信模型"

    def _get_host_value(self):
        """获取host"""
        host = self.env['ir.config_parameter'].sudo().get_param('hd_sms_host') or ''
        return host

    def _get_port_value(self):
        """获取port"""
        port = self.env['ir.config_parameter'].sudo().get_param('hd_sms_port') or 0

        return port

    def _get_sin_value(self):
        """获取sig url"""
        single_url = self.env['ir.config_parameter'].sudo().get_param('sms_single_url') or ''
        return single_url

    def _get_batch_value(self):
        """获取sig url"""
        batch_url = self.env['ir.config_parameter'].sudo().get_param('sms_batch_url') or ''
        return batch_url

    def _get_tpl_value(self):
        """获取sig url"""
        tpl_url = self.env['ir.config_parameter'].sudo().get_param('sms_tpl_url') or ''
        return tpl_url

    def _get_appkey_value(self):
        """获取sig url"""
        appkey = self.env['ir.config_parameter'].sudo().get_param('hd_sms_appkey') or ''
        return appkey

    name = fields.Char(u'名称')
    host = fields.Char(u'服务地址', default=_get_host_value)
    port = fields.Integer(u'端口', default=_get_port_value)
    type = fields.Selection([('bs_sms', u'指定文本短信'), ('tpl_sms', u'指定模板短信')], string=u'短信模板类型', default='bs_sms')
    sin_url = fields.Char(u'单条短信接口的URl', help=u'填写格式例：/v2/sms/single_send.json', default=_get_sin_value)
    batch_url = fields.Char(u'批量短信接口的URl', default=_get_batch_value)
    tpl_url = fields.Char(u'模板短信接口的URl', default=_get_tpl_value)
    notes = fields.Text(u'描述')
    apikey = fields.Char(u'API Key', default=_get_appkey_value)

    # 指定文本测试
    test_mobile = fields.Char(u'测试手机号',groups="base.group_system")
    test_content = fields.Char(u'短信模板内容', help=u'此内容必须提前在云片上配置好')

    # 指定模板测试
    tpl_id = fields.Integer(U'tpl id')
    tpl_value = fields.Text(u'指定模板内容', help=u"{'#usertruename#': usertruename, '#visitwebsite#': visitwebsite}")

    def send_singl_sms(self, text, mobile, model_name):
        """
        通用接口发短信;
        功能：1、发送短信到手机;
             2、记录短信消息；
        """
        parm_obj = self.env['ir.config_parameter']
        order_boj = self.env['hd.sms.order']
        host = parm_obj.sudo().get_param('hd_sms_host')
        port = parm_obj.sudo().get_param('hd_sms_port')
        single_url = parm_obj.sudo().get_param('sms_single_url')
        apikey = parm_obj.sudo().get_param('hd_sms_appkey')
        params = urllib.parse.urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
        conn = http.client.HTTPSConnection(host, port=port, timeout=30)
        conn.request("POST", single_url, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        result = json.loads(response_str)
        conn.close()
        # 将发送的短信记录到表单里面
        state = 'success'
        if result.get('code') != 0:
            state = 'fail'
        order_boj.create({'mobile': mobile,
                          'name': text,
                          'order_date': datetime.datetime.now(),
                          'models_name': model_name,
                          'state': state,
                          'back_content': result
                          })
        return result

    def send_batch_sms(self, text, mobile, model_name):
        """
        通用接口发短信
        批量发送相同内容的短信

        """
        parm_obj = self.env['ir.config_parameter']
        order_boj = self.env['hd.sms.order']
        host = parm_obj.sudo().get_param('hd_sms_host')
        port = parm_obj.sudo().get_param('hd_sms_port')
        batch_url = parm_obj.sudo().get_param('sms_batch_url')
        apikey = parm_obj.sudo().get_param('hd_sms_appkey')
        params = urllib.parse.urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
        conn = http.client.HTTPSConnection(host, port=port, timeout=30)
        conn.request("POST", batch_url, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        result = json.loads(response_str)
        conn.close()
        # 将发送的短信记录到表单里面,批量发送要区分发送成功和失败
        success_value = []
        success_mobile = []
        fail_value = []
        fail_mobile = []
        for line in result['data']:
            if line['code'] in [0, '0']:
                success_value.append(line)
                success_mobile.append(line['mobile'])
            else:
                fail_value.append(line)
                fail_mobile.append(line['mobile'])
        if success_value:
            values = {
                'name': text,
                'order_date': datetime.datetime.now(),
                'models_name': model_name,
                'mobile': ','.join(success_mobile),
                'state': 'success',
                'back_content': success_value
            }
            order_boj.create(values)
        if fail_value:
            values = {
                'name': text,
                'order_date': datetime.datetime.now(),
                'models_name': model_name,
                'mobile': ','.join(fail_mobile),
                'state': 'fail',
                'back_content': fail_value
            }
            order_boj.create(values)
        return result

    def tpl_send_sms(self, tpl_id, tpl_value, mobile, model_name):
        """
        模板接口发短信
        """
        parm_obj = self.env['ir.config_parameter']
        order_boj = self.env['hd.sms.order']
        host = parm_obj.sudo().get_param('hd_sms_host')
        port = parm_obj.sudo().get_param('hd_sms_port')
        tpl_url = parm_obj.sudo().get_param('sms_tpl_url')
        apikey = parm_obj.sudo().get_param('hd_sms_appkey')
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
        conn = http.client.HTTPSConnection(host, port=port, timeout=30)
        conn.request("POST", tpl_url, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        result = json.loads(response_str)
        conn.close()
        # 将发送的短信记录到表单里面
        state = 'success'
        if result.get('code') != 0:
            state = 'fail'
        order_boj.create({'mobile': mobile,
                          'name': tpl_value,
                          'order_date': datetime.datetime.now(),
                          'models_name': model_name,
                          'state': state,
                          'back_content': result
                          })
        return result

    def btm_test_sin_sms(self):
        """
        :return:
        key：fd7dc272d66a719644ce4991e0d50c56
        # 调用模板接口发短信
        tpl_id = 4825616  # 对应的模板内容为：您的验证码是#code#【#company#】
        tpl_value = {'#usertruename#': usertruename, '#visitwebsite#': visitwebsite,
                     '#username#': username,'#password#': password, '#deadline#': deadline}
        """
        # 调用智能匹配模板接口发短信
        model_name = '云片短信模块'
        result = self.send_singl_sms(self.test_content, self.test_mobile, model_name)
        msg_type = 'success'
        ret_sms = result.get('msg')
        if result.get('code') != 0:
            msg_type = 'warning'
        self.notes = result
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '云片短信发送',
                'sticky': True,
                'type': msg_type,
                'message': _(ret_sms),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def btm_test_batch_sms(self):
        """
        :return:
        text =
        """
        # 调用智能匹配模板接口发短信
        model_name = '云片短信模块'
        result = self.send_batch_sms(self.test_content, self.test_mobile, model_name)
        success_mobile = []
        fail_mobile = []
        for line in result['data']:
            if line['code'] in [0, '0']:
                success_mobile.append(line['mobile'])
            else:
                fail_mobile.append(line['mobile'])
        message = '短信发送成功的号码有：%s,发送失败的号码有：%s' % (','.success_mobile, ','.fail_mobile)
        self.notes = message
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '云片短信发送',
                'sticky': True,
                'message': _(message),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def btm_test_tpl_sms(self):
        """
        :return:
        key：fd7dc272d66a719644ce4991e0d50c56
        # 调用模板接口发短信
        tpl_id = 4825616  # 对应的模板内容为：您的验证码是#code#【#company#】
        tpl_value = {'#usertruename#': usertruename, '#visitwebsite#': visitwebsite,
                     '#username#': username,'#password#': password, '#deadline#': deadline}
        """
        tpl_id = '4825616'
        tpl_value = {'#usertruename#': 'test', '#visitwebsite#': 'www.baidu.com',
                     '#username#': 'melon', '#password#': '123456', '#deadline#': '2021-11-10'}
        model_name = '云片短信模块'
        result = self.tpl_send_sms(tpl_id, tpl_value, self.test_mobile, model_name)
        msg_type = 'success'
        ret_sms = result.get('msg')
        if result.get('code') != 0:
            msg_type = 'warning'
        self.notes = result
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'tpl云片短信',
                'sticky': True,
                'type': msg_type,
                'message': _(ret_sms),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
