# -*- coding: utf-8 -*-
import odoo
from odoo import api, fields, models, tools
import logging
from threading import Thread

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    model = fields.Char(u'规格型号')
