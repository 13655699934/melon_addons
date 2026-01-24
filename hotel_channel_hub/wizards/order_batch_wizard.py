# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class OrderBatchWizard(models.TransientModel):
    """批量处理订单向导"""
    _name = 'order.batch.wizard'
    _description = '批量处理订单'

    order_ids = fields.Many2many('hotel.order', string='订单', required=True)
    action = fields.Selection([
        ('confirm', '批量确认'),
        ('cancel', '批量取消'),
        ('checkin', '批量入住'),
        ('checkout', '批量退房'),
    ], string='操作', required=True, default='confirm')
    
    cancel_reason = fields.Text('取消原因')
    
    # 统计
    order_count = fields.Integer('订单数', compute='_compute_order_count')

    @api.depends('order_ids')
    def _compute_order_count(self):
        """计算订单数"""
        for wizard in self:
            wizard.order_count = len(wizard.order_ids)

    def action_process(self):
        """执行批量处理"""
        self.ensure_one()
        
        if not self.order_ids:
            raise exceptions.UserError(_('请选择要处理的订单！'))
        
        success_count = 0
        failed_orders = []
        
        for order in self.order_ids:
            try:
                if self.action == 'confirm':
                    if order.state == 'draft':
                        order.action_confirm()
                        success_count += 1
                    else:
                        failed_orders.append(f"{order.name} (状态: {order.state})")
                
                elif self.action == 'cancel':
                    if order.state in ['draft', 'confirmed']:
                        if self.cancel_reason:
                            order.write({'cancel_reason': self.cancel_reason})
                        order.action_cancel()
                        success_count += 1
                    else:
                        failed_orders.append(f"{order.name} (状态: {order.state})")
                
                elif self.action == 'checkin':
                    if order.state == 'confirmed':
                        order.action_checkin()
                        success_count += 1
                    else:
                        failed_orders.append(f"{order.name} (状态: {order.state})")
                
                elif self.action == 'checkout':
                    if order.state == 'checked_in':
                        order.action_checkout()
                        success_count += 1
                    else:
                        failed_orders.append(f"{order.name} (状态: {order.state})")
            
            except Exception as e:
                failed_orders.append(f"{order.name} (错误: {str(e)})")
        
        # 返回结果通知
        message = _('成功处理 %d 个订单') % success_count
        if failed_orders:
            message += _('\n\n失败的订单:\n') + '\n'.join(failed_orders)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('批量处理完成'),
                'message': message,
                'type': 'success' if not failed_orders else 'warning',
                'sticky': True,
            }
        }

    @api.model
    def default_get(self, fields_list):
        """从上下文获取默认订单"""
        res = super().default_get(fields_list)
        
        # 从上下文获取选中的订单
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['order_ids'] = [(6, 0, active_ids)]
        
        return res

