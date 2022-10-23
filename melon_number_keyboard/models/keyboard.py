# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import datetime,timedelta
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class VirtualKeyboard(models.Model):
    _name = 'virtual.keyboard'
    _description = '''虚拟数字键盘'''

    name = fields.Char(string='name')
    virtual_float =  fields.Float(string='测试float')
    virtual_integer =  fields.Integer(string='测试integer')
    
    def btn_virtual_keyboard(self):
        return {
            'type':'ir.actions.act_window',
            'name':'keyboard',
            'res_model':'virtual.keyword.wizard',
            'view_mode':'form',
            'target':'new',
            'context':{'res_id':self.id}
        }
