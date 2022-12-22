# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    fapiao = fields.Char(string='发票号', copy=False, tracking=True, size=100000)
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
        ('all', 'all'),
    ], compute='_compute_partner_type', tracking=True, store=True)
    state = fields.Selection(selection_add=[
        ('draft',),
        ('to_approved', '待审批'),
        ('approved', '已审批'),
        ('posted',)
    ], ondelete={'to_approved': 'set default', 'approved': 'set default'})
    melon_manager_id = fields.Many2one('res.users', string=u'审核人')
    melon_post_id = fields.Many2one('res.users', string=u'过账人', compute='_compute_melon_post_id', store=True)



    @api.depends('state')
    def _compute_melon_post_id(self):
        for order in self:
            melon_post_id = False
            # melon_code = ''
            if order.state == 'posted':
                melon_post_id = self.env.user
                # melon_code = self.env['ir.sequence'].next_by_code('account.move.melon')
            order.melon_post_id = melon_post_id
            # order.melon_code = melon_code

    def btn_to_approval(self):
        """提交审批"""
        if self.state == 'draft':
            self.write({'state': 'to_approved'})

    def btn_to_refuse(self):
        """提交审批"""
        if self.state == 'to_approved':
            self.write({'state': 'draft'})

    def btn_approved(self):
        """经理审批"""
        if self.state == 'to_approved':
            self.write({'state': 'approved', 'melon_manager_id': self.env.user})

    @api.depends('move_type')
    def _compute_partner_type(self):
        for order in self:
            partner_type = ''
            if order.move_type in ['out_invoice', 'out_refund', 'out_receipt']:
                partner_type = 'customer'
            if order.move_type in ['in_invoice', 'in_refund', 'in_receipt']:
                partner_type = 'supplier'
            if order.move_type == 'entry':
                partner_type = 'all'
            order.partner_type = partner_type

    @api.constrains('fapiao')
    def _check_fapiao(self):
        for record in self:
            if record.fapiao and (len(record.fapiao) != 8 or not record.fapiao.isdecimal()):
                pass


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    desc_length = fields.Boolean(u'长度', compute='_compute_description_length', store=True)

    @api.depends('name')
    def _compute_description_length(self):
        for order in self:
            melon_length = False
            if order.name:
                if len(order.name) >= 33:
                    melon_length = True
            order.desc_length = melon_length
