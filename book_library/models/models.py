# -*- coding: utf-8 -*-
from datetime import date, datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Book(models.Model):
    _name = 'melon.book'
    _description = "书籍"
    _inherit = ['mail.thread']

    name = fields.Char('名称')
    display_name = fields.Char('显示名称', compute='_compute_display_name', store=True)
    author = fields.Char('作者')
    date = fields.Date("出版日期")
    price = fields.Float("定价")
    qty = fields.Integer("图书数量")
    image_128 = fields.Image("Image(128)", max_width=128, max_height=128)
    file = fields.Binary('File')
    filename = fields.Char('File Name')
    note = fields.Text('备注')
    description = fields.Html('Description')
    date_start = fields.Datetime("录入时间", default=fields.Datetime.now())
    state = fields.Selection([
        ('on_sale', '在售'),
        ('sell_out', '售罄'),
        ('lower_shelf', '下架')
    ], string='状态', index=True, readonly=True, copy=False, default='on_sale')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', "书名必须唯一"),
    ]

    @api.model
    def create(self, vals):
        return super(Book, self).create(vals)

    @api.constrains('name', 'date')
    def _check_name(self):
        """检查名称长度"""
        if len(self.name) > 10:
            raise ValidationError("图书名称必须限制在10个字符以内")
        if self.date < date(2000, 1, 1):
            raise ValidationError("只能添加2000年以后的图书")

    @api.depends('name', 'author')
    def _compute_display_name(self):
        """组合显示名称"""
        for order in self:
            if order.name and order.author:
                order.display_name = '%s-%s' % (order.name or '', order.author or '')

    def action_open_book_detail(self):
        """打开图书列表，查看详情 """
        return {
            'type': 'ir.actions.act_url',
            'name': "Book List",
            'target': 'self',
            'url': '/book_library/book_library/objects/',
        }

    def btn_sell_out(self):
        self.write({'state': 'sell_out'})

    def btn_lower_shelf(self):
        self.write({'state': 'lower_shelf'})

    def btn_on_sale(self):
        self.write({'state': 'on_sale'})


    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        raise UserError('您不能复制图书！')