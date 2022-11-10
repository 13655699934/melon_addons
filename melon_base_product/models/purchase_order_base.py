# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    project_name = fields.Char(u'项目')


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    model = fields.Char(u'规格型号', related='product_id.model')
