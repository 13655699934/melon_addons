# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
import datetime
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentMelon(models.Model):
    _inherit = "account.payment"

    # 应付合计（动态）：取值逻辑是：账单总金额 - 对应的供应商总付款 = 应付账款余额
    # 应付合计（静态）：取值逻辑是: 创建单据当天账单总金额 - 对应的供应商当天的总付款 = 应付账款余额
    total_payable_dyn = fields.Float(u'应付合计(动态)', compute='_compute_total_payable_dyn')
    total_payable_static = fields.Float(u'应付合计(静态)', compute='_compute_total_payable_static', store=True)

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
            self.write({'state': 'approved'})

    # 旧的逻辑
    def _compute_total_payable_dyn(self):
        for order in self:
            amount_move_obj = self.env['account.move']
            amount_line_obj = self.env['account.move.line']
            account_obj = self.env['account.account']
            amount_pay_obj = self.env['account.payment']
            total_payable_dyn = 0.0
            if order.partner_id:
                # 应付账款
                account_id = account_obj.search([('code', '=', '220200')], limit=1)

                # 期初 ：借方
                begin_debit_amount = 0.0
                # 贷方
                begin_credit_amount = 0.0
                begin_amount_id = amount_line_obj.search(
                    [('partner_id', '=', order.partner_id.id), ('ref', '=', '期初'),
                     ('parent_state', '=', 'posted'),
                     ('account_id', '=', account_id.id)], limit=1)
                if begin_amount_id:
                    begin_debit_amount = begin_amount_id.debit
                    begin_credit_amount = begin_amount_id.credit
                # 账单总金额[('move_type', '=', 'in_invoice')]
                total_amount = 0.0
                amount_ids = amount_move_obj.search(
                    [('partner_id', '=', order.partner_id.id), ('move_type', '=', 'in_invoice'),
                     ('state', '=', 'posted')])
                if amount_ids:
                    total_amount = sum(amount_ids.mapped("amount_total"))
                # 总的付款
                pay_ids = amount_pay_obj.search(
                    [('partner_id', '=', order.partner_id.id), ('payment_type', '=', 'outbound'),
                     ('state', '=', 'posted')])
                total_pay = 0.0
                if pay_ids:
                    total_pay = sum(pay_ids.mapped("amount"))
                # 应付合计（动态）
                total_payable_dyn = total_amount - begin_debit_amount - total_pay
            order.total_payable_dyn = abs(total_payable_dyn)

    @api.depends('date')
    def _compute_total_payable_static(self):
        for order in self:
            amount_move_obj = self.env['account.move']
            amount_line_obj = self.env['account.move.line']
            account_obj = self.env['account.account']
            amount_pay_obj = self.env['account.payment']
            total_payable_static = 0.0
            TODAY = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if order.partner_id:
                # 应付账款
                account_id = account_obj.search([('code', '=', '220200')], limit=1)
                # 期初 ：借方
                begin_debit_amount = 0.0
                # 贷方
                begin_credit_amount = 0.0
                begin_amount_id = amount_line_obj.search(
                    [('partner_id', '=', order.partner_id.id), ('ref', '=', '期初'),
                     ('parent_state', '=', 'posted'),
                     ('account_id', '=', account_id.id)], limit=1)
                if begin_amount_id:
                    begin_debit_amount = begin_amount_id.debit
                    begin_credit_amount = begin_amount_id.credit
                # 账单总金额
                total_amount = 0.0
                amount_ids = amount_move_obj.search(
                    [('partner_id', '=', order.partner_id.id), ('move_type', '=', 'in_invoice'),
                     ('state', '=', 'posted'),
                     ('write_date', '<=', TODAY)])
                if amount_ids:
                    total_amount = sum(amount_ids.mapped("amount_total"))

                # 总的付款payment_type': 'outbound',
                pay_ids = amount_pay_obj.search(
                    [('partner_id', '=', order.partner_id.id), ('payment_type', '=', 'outbound'),
                     ('state', '=', 'posted'), ('write_date', '<=', TODAY)])
                total_pay = 0.0
                if pay_ids:
                    total_pay = sum(pay_ids.mapped("amount"))
                # 应付合计（静态）
                total_payable_static = total_amount - begin_debit_amount - total_pay
            order.total_payable_static = abs(total_payable_static)

    @api.onchange('payment_type')
    def onchange_payment_type(self):
        if self.payment_type:
            if self.payment_type == 'outbound':
                self.partner_type = 'supplier'
            else:
                self.partner_type = 'customer'
