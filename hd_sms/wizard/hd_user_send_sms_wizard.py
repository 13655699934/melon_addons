# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
import datetime


class HdApikeySendSmsWizard(models.TransientModel):
    _name = 'hd.apikey.send.sms.wizard'
    _description = '短信发送'

    def _get_default_mobile(self):
        mobile = self.env.context.get('mobile') or None
        return mobile

    def _get_default_usertruename(self):
        username = self.env.context.get('username') or None
        return username

    apikey = fields.Char('管理员配置apikey', default='fd7dc272d66a719644ce4991e0d50c569')
    mobile = fields.Char('手机', default=_get_default_mobile, store=True)
    username = fields.Char('用户名', default='melon')
    password = fields.Char('密码', default='123456')
    tpl_id = fields.Integer('tpl_id', default=4825616)
    visitwebsite = fields.Char('地址', default='http://www.baidu.com')
    deadline = fields.Date(string='最后期限', tracking=True,
                           default=datetime.datetime.strptime("2999-12-31", '%Y-%m-%d'))
    msm_text = fields.Text('内容', default='测试数据111')
    usertruename = fields.Char('名称', default=_get_default_usertruename, store=True)

    # def btm_confirm_sms_method(self):
    #     yp_demo.get_user_info(self.apikey)
    #     tpl_value = {'#usertruename#': self.usertruename, '#visitwebsite#': self.visitwebsite,
    #                  '#username#': self.username,
    #                  '#password#': self.password, '#deadline#': self.deadline}
    #     # 调用智能匹配模板接口发短信
    #     yp_demo.send_sms(self.apikey, self.msm_text, self.mobile)
    #     yp_demo.tpl_send_sms(self.apikey, self.tpl_id, tpl_value, self.mobile)
