# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand = fields.Char(u'品牌')
    model = fields.Char(u'规格型号')
    map_number = fields.Char(u'图号')
    hs_code = fields.Char(u'HS编码')
    remark_message = fields.Text(u'备注')
    second_uom_id = fields.Many2one('uom.uom', string=u'第二计量单位')
    fix_price = fields.Float(u'标准成本')
    purchase_method = fields.Selection([('purchase', '订购数量'), ('receive', '收到数量')], string=u'控制采购账单')
    state = fields.Selection([('draft', '草稿'), ('approval', '提交审批'), ('approved', '已审批')], string=u'审批状态',
                             default='draft')



class ProductCategory(models.Model):
    _inherit = 'product.category'

    type = fields.Selection([('view', '查看'), ('normal', '一般')], string=u'类别类型')
