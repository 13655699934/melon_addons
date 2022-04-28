# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _


class Partner(models.Model):
    _inherit = 'res.partner'

    # name = fields.Char(u'名称')
    # mobile = fields.Char(u'手机')
    # work_email = fields.Char(u'邮箱')
