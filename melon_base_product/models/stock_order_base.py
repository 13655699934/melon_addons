# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
import logging

_logger = logging.getLogger(__name__)




class StockMove(models.Model):
    _inherit = 'stock.move'

    model = fields.Char(u'规格型号', related='product_id.model')
