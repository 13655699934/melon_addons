# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project',string=u'项目')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    model = fields.Char(u'规格型号', related='product_id.model')


