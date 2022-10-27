# -*- coding: utf-8 -*-

import base64
import io
import re
from io import BytesIO
from odoo import models, fields, api
import qrcode
from PIL import Image


class DynamicOrder(models.Model):
    _name = 'dynamic.order'
    _description = '测试'


    name = fields.Char(u'编号')
    state = fields.Selection([
        ('启用', '启用'),
        ('待机', '待机'),
        ('停用', '停用')],
        u'当前状态', default='启用')
    test1=fields.Char(u'test1')

    @api.model
    def create(self, vals):
        return super(DynamicOrder, self).create(vals)
