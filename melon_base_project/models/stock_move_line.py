# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    amount_total = fields.Float(u'总金额', compute='_compute_amount_total', store=False)
    standard_price = fields.Float(u'成本价',related='product_id.standard_price', store=True)

    def _compute_amount_total(self):
        for order in self:
            amount_total = 0.0
            if order.qty_done:
                amount_total = order.qty_done * order.standard_price
            order.amount_total = amount_total
