# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one('project.project',string=u'项目')

    @api.model
    def create(self,vals):
        res=super(StockPicking, self).create(vals)
        if res.sale_id and res.sale_id.project_id:
           res.project_id =res.sale_id.project_id.id
        return  res



