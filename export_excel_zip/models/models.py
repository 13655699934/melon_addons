# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import models, fields, tools, _

class demo_user(models.Model):
    _name = 'demo.user'
    _description = '用户'

    name = fields.Char('姓名')
    sex = fields.Char('性别')
    age = fields.Integer('年龄')
