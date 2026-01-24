# -*- coding: utf-8 -*-

import secrets
from datetime import datetime, timedelta
from odoo import models, fields, api, exceptions, _


class Channel(models.Model):
    """销售渠道模型"""
    _name = 'hotel.channel'
    _description = '销售渠道'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('渠道名称', required=True, tracking=True)
    code = fields.Char('渠道编码', required=True, copy=False, index=True)
    enterprise_key = fields.Char('企业唯一标识', required=True, copy=False, index=True,
                                  help='用于企业/渠道端集成的唯一标识')
    
    # Token 相关
    token = fields.Char('访问Token', copy=False, readonly=True, groups='base.group_system')
    token_expiry = fields.Datetime('Token过期时间', readonly=True)
    
    # 集成设置
    callback_url = fields.Char('回调URL', help='接收订单变更通知的URL')
    webhook_secret = fields.Char('Webhook密钥', copy=False)
    
    # 状态
    active = fields.Boolean('启用', default=True, tracking=True)
    last_sync_date = fields.Datetime('最近同步时间', readonly=True)
    
    # 统计
    order_count = fields.Integer('订单数', compute='_compute_order_count')
    sync_log_count = fields.Integer('同步日志数', compute='_compute_sync_log_count')
    
    company_id = fields.Many2one('res.company', '公司', default=lambda self: self.env.company)
    
    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id)', '同一公司下渠道编码必须唯一！'),
        ('enterprise_key_uniq', 'unique(enterprise_key)', '企业唯一标识必须唯一！'),
    ]

    def _compute_order_count(self):
        """计算订单数量"""
        for channel in self:
            channel.order_count = self.env['hotel.order'].search_count([('channel_id', '=', channel.id)])

    def _compute_sync_log_count(self):
        """计算同步日志数量"""
        for channel in self:
            channel.sync_log_count = self.env['hotel.sync.log'].search_count([('channel_id', '=', channel.id)])

    @api.model
    def generate_token(self):
        """生成随机Token（32字符）"""
        return secrets.token_urlsafe(32)

    def action_generate_token(self):
        """手动生成/轮换Token"""
        for channel in self:
            token = self.generate_token()
            expiry = datetime.now() + timedelta(days=365)  # Token 有效期1年
            channel.write({
                'token': token,
                'token_expiry': expiry,
            })
            # 记录日志
            channel.message_post(
                body=f'Token已重新生成，过期时间: {expiry.strftime("%Y-%m-%d %H:%M:%S")}',
                subject='Token轮换'
            )

    @api.model
    def get_channel_by_enterprise_key(self, enterprise_key):
        """根据企业标识获取渠道"""
        return self.search([('enterprise_key', '=', enterprise_key), ('active', '=', True)], limit=1)

    def validate_token(self, token):
        """
        验证Token是否有效
        :param token: 待验证的Token
        :return: Boolean
        """
        self.ensure_one()
        
        if not self.active:
            return False
        
        if self.token != token:
            return False
        
        # 检查是否过期
        if self.token_expiry and self.token_expiry < datetime.now():
            return False
        
        # 更新最近同步时间
        self.sudo().write({'last_sync_date': fields.Datetime.now()})
        
        return True

    def action_view_orders(self):
        """查看该渠道的所有订单"""
        self.ensure_one()
        return {
            'name': f'{self.name} - 订单列表',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.order',
            'view_mode': 'list,form,calendar',
            'domain': [('channel_id', '=', self.id)],
            'context': {'default_channel_id': self.id}
        }

    def action_view_sync_logs(self):
        """查看同步日志"""
        self.ensure_one()
        return {
            'name': f'{self.name} - 同步日志',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.sync.log',
            'view_mode': 'list,form',
            'domain': [('channel_id', '=', self.id)],
            'context': {'default_channel_id': self.id}
        }

    @api.model
    def create(self, vals):
        """创建时自动生成Token"""
        if not vals.get('token'):
            vals['token'] = self.generate_token()
            vals['token_expiry'] = datetime.now() + timedelta(days=365)
        return super().create(vals)

