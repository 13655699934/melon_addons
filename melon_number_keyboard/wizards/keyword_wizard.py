# -*- coding: utf-8 -*-

from odoo import fields, models, api


class VirtualKeywordWizard(models.TransientModel):
    _name = "virtual.keyword.wizard"
    _description = "向导"


    name = fields.Char('name')
    virtual_float = fields.Float(string='测试float')
    virtual_integer = fields.Integer(string='测试integer')
