# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ApplicationContent(models.Model):
    _name = 'application.content.type'
    _description = '应用内容分类'

    name = fields.Char(u'名称')
