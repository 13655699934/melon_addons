# -*- coding: utf-8 -*-

import json
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class SyncLog(models.Model):
    """同步日志模型"""
    _name = 'hotel.sync.log'
    _description = '同步日志'
    _order = 'create_date desc, id desc'

    name = fields.Char('日志标题', compute='_compute_name', store=True)
    channel_id = fields.Many2one('hotel.channel', '渠道', ondelete='set null', index=True)
    
    # 操作信息
    operation = fields.Selection([
        ('token_get', '获取Token'),
        ('room_query', '查询房间'),
        ('order_create', '创建订单'),
        ('order_update', '更新订单'),
        ('order_cancel', '取消订单'),
        ('order_confirm', '确认订单'),
        ('availability_update', '更新库存'),
        ('price_update', '更新价格'),
        ('webhook', 'Webhook回调'),
        ('sync', '数据同步'),
        ('other', '其他'),
    ], string='操作类型', required=True, index=True)
    
    # 关联订单
    order_id = fields.Many2one('hotel.order', '关联订单', ondelete='set null')
    
    # 状态与结果
    status = fields.Selection([
        ('success', '成功'),
        ('failed', '失败'),
        ('pending', '处理中'),
    ], string='状态', default='pending', required=True, index=True)
    
    message = fields.Text('消息')
    error_message = fields.Text('错误信息')
    
    # 请求与响应
    request_data = fields.Text('请求数据')
    response_data = fields.Text('响应数据')
    
    # 性能
    duration = fields.Float('耗时(秒)', digits=(10, 3))
    
    # IP与用户
    ip_address = fields.Char('IP地址')
    user_id = fields.Many2one('res.user', '用户', default=lambda self: self.env.user)
    
    company_id = fields.Many2one('res.company', '公司', default=lambda self: self.env.company)

    @api.depends('operation', 'channel_id.name', 'status')
    def _compute_name(self):
        """计算日志标题"""
        operation_dict = dict(self._fields['operation'].selection)
        for log in self:
            parts = []
            if log.channel_id:
                parts.append(log.channel_id.name)
            parts.append(operation_dict.get(log.operation, log.operation))
            if log.status:
                status_dict = dict(self._fields['status'].selection)
                parts.append(status_dict.get(log.status, log.status))
            log.name = ' - '.join(parts)

    @api.model
    def log_api_call(self, operation, channel_id=None, status='success', 
                     message='', error_message='', request_data=None, 
                     response_data=None, duration=0, order_id=None, ip_address=None):
        """
        记录API调用日志
        :param operation: 操作类型
        :param channel_id: 渠道ID
        :param status: 状态
        :param message: 消息
        :param error_message: 错误信息
        :param request_data: 请求数据（dict）
        :param response_data: 响应数据（dict）
        :param duration: 耗时
        :param order_id: 订单ID
        :param ip_address: IP地址
        :return: 日志记录
        """
        vals = {
            'operation': operation,
            'channel_id': channel_id,
            'status': status,
            'message': message,
            'error_message': error_message,
            'duration': duration,
            'order_id': order_id,
            'ip_address': ip_address,
        }
        
        # 序列化请求和响应数据
        if request_data:
            vals['request_data'] = json.dumps(request_data, ensure_ascii=False, indent=2)
        if response_data:
            vals['response_data'] = json.dumps(response_data, ensure_ascii=False, indent=2)
        
        return self.create(vals)

    def action_view_order(self):
        """查看关联订单"""
        self.ensure_one()
        if not self.order_id:
            return
        
        return {
            'name': '订单详情',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.order',
            'res_id': self.order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def _cron_clean_old_logs(self):
        """
        定时任务：清理过期日志
        删除30天前的日志记录
        """
        from datetime import datetime, timedelta
        
        # 计算30天前的日期
        cutoff_date = datetime.now() - timedelta(days=30)
        
        # 查找并删除过期日志
        old_logs = self.search([
            ('create_date', '<', cutoff_date)
        ])
        
        count = len(old_logs)
        if count > 0:
            old_logs.unlink()
            _logger.info(f'定时任务：已清理 {count} 条过期日志')
        
        return True

