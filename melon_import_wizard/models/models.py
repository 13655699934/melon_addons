from odoo import fields, models, api, _


class DateOrder(models.Model):
    _name = 'melon.data.order'
    _description = '测试'

    name = fields.Char(string='名称')
    code = fields.Char(string="编号")
    order_name = fields.Char(string=u'描述')
    ded_expenses = fields.Float(string='费用')
    close_amount = fields.Float(string='金额')
    notes = fields.Char(string='备注')
