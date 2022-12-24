# -*- coding: utf-8 -*-
import http.client
import urllib
import json
from odoo import api, fields, models, _
import datetime


class HdSmsTemplates(models.Model):
    _name = "hd.sms.templates"
    _description = "短信模板"

    name = fields.Char(u'模板代码')
    type = fields.Selection([('bs_sms', u'指定文本'), ('tpl_sms', u'指定模板')], string=u'短信模板类型', default='bs_sms')
    tpl_id = fields.Char(u'指定模板ID')
    tpl_content = fields.Text(u'指定模板内容')
    single_content = fields.Text(u'指定文本内容')
    tmp_desc = fields.Text(u'模板描述')

    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hd.sms.templates') or _('New')
        return super(HdSmsTemplates, self).create(vals)
