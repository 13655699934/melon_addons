# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    standard_price = fields.Float(u'成本价', related='product_id.standard_price', store=False)
    amount_total = fields.Float(u'总金额(new)', compute='_compute_amount_total', store=False)


    def _compute_amount_total(self):
        for order in self:
            amount_total = 0.0
            if order.quantity:
                amount_total = order.quantity * order.standard_price
            order.amount_total = amount_total
