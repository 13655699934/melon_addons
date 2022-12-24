# -*- coding: utf-8 -*-
import http.client
import urllib
import json
from odoo import api, fields, models, _
import datetime


class HdSmsOrder(models.Model):
    _name = "hd.sms.order"
    _description = "发送短信模型"

    mobile = fields.Char(u'手机号')
    name = fields.Text(u'发送内容')
    order_date = fields.Datetime(u'发送时间')
    models_name = fields.Char(u'模块名称')
    state = fields.Selection([('success', u'发送成功'), ('fail', u'失败')], string=u'发送状态')
    back_content= fields.Text(u'返回值')







