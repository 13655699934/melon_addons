# -*- coding: utf-8 -*-
from odoo import models, fields, tools, api
import logging

_logger = logging.getLogger(__name__)


class WatermarkDesignOrder(models.Model):
    _name = "watermark.design.order"
    _description = "水印设置"

    name = fields.Char(string=u'水印内容')
    colorpicker = fields.Char(string=u'颜色')
    font_size = fields.Integer(string=u'字体大小', default=20)
    show_date = fields.Boolean(u'显示当天日期')

    test_data = fields.Binary('下载查看附件')
    test_filename = fields.Char('测试附件名')

