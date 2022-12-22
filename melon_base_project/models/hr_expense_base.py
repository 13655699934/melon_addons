# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
import logging

_logger = logging.getLogger(__name__)


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    move_line_ids = fields.Many2many('account.move.line', string=u'日记账项目')
