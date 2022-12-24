# -*- coding: utf-8 -*-


from dateutil import tz

from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval, datetime


class AuditLogs(models.Model):
    _name = 'audit.logs'
    _description = '操作日志'
    _order = 'create_date desc, id desc'

    name = fields.Char(string=u'操作名称', copy=False, readonly=True, index=True)
    model_id = fields.Many2one('ir.model', '数据模型', readonly=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', '用户', required=True, readonly=True)
    url = fields.Char(string=u'URL', required=True, copy=False, readonly=True)
    ipaddress = fields.Char(string=u'操作IP地址', required=True, copy=False, readonly=True)
    model_method = fields.Char(string=u'操作方式', copy=False, readonly=True)
    result = fields.Char(string=u'操作结果', required=True, copy=False, readonly=True)
    params = fields.Text(string=u'操作参数')
    data_html = fields.Html('变更信息', readonly=True)
