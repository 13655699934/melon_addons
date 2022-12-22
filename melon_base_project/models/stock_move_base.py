# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)




class StockMove(models.Model):
    _inherit = 'stock.move'

    model = fields.Char(u'规格型号', related='product_id.model')

