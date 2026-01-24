# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta


class RoomPriceWizard(models.TransientModel):
    """批量更新房间价格向导"""
    _name = 'room.price.wizard'
    _description = '批量更新房间价格'

    hotel_id = fields.Many2one('hotel.hotel', '酒店', required=True)
    room_type_id = fields.Many2one('hotel.room.type', '房型',
                                    domain="[('hotel_id', '=', hotel_id)]")
    room_ids = fields.Many2many('hotel.room', string='房间',
                                 domain="[('hotel_id', '=', hotel_id)]")
    
    # 日期范围
    date_from = fields.Date('开始日期', required=True, default=fields.Date.today)
    date_to = fields.Date('结束日期', required=True,
                           default=lambda self: fields.Date.today() + timedelta(days=30))
    
    # 更新选项
    update_type = fields.Selection([
        ('price', '仅更新价格'),
        ('quota', '仅更新库存'),
        ('both', '更新价格和库存'),
    ], string='更新类型', default='both', required=True)
    
    # 价格设置
    price = fields.Float('价格', digits='Product Price')
    price_adjustment = fields.Selection([
        ('set', '设置为固定值'),
        ('increase', '增加'),
        ('decrease', '减少'),
        ('percent', '按百分比调整'),
    ], string='价格调整方式', default='set')
    price_value = fields.Float('调整值', digits='Product Price')
    
    # 库存设置
    quota = fields.Integer('库存')
    
    # 状态
    is_open = fields.Boolean('开放售卖', default=True)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        """检查日期"""
        for wizard in self:
            if wizard.date_to < wizard.date_from:
                raise exceptions.ValidationError(_('结束日期必须大于等于开始日期！'))

    @api.onchange('hotel_id')
    def _onchange_hotel_id(self):
        """切换酒店时清空房型和房间"""
        self.room_type_id = False
        self.room_ids = False

    def action_update(self):
        """执行批量更新"""
        self.ensure_one()
        
        # 获取要更新的房间列表
        if self.room_ids:
            rooms = self.room_ids
        elif self.room_type_id:
            rooms = self.env['hotel.room'].search([
                ('hotel_id', '=', self.hotel_id.id),
                ('room_type_id', '=', self.room_type_id.id),
                ('active', '=', True),
            ])
        else:
            rooms = self.env['hotel.room'].search([
                ('hotel_id', '=', self.hotel_id.id),
                ('active', '=', True),
            ])
        
        if not rooms:
            raise exceptions.UserError(_('没有找到要更新的房间！'))
        
        # 生成日期列表
        current_date = self.date_from
        dates = []
        while current_date <= self.date_to:
            dates.append(current_date)
            current_date += timedelta(days=1)
        
        # 批量更新
        Availability = self.env['hotel.room.availability']
        updated_count = 0
        
        for room in rooms:
            for date in dates:
                # 获取或创建库存记录
                avail = Availability.get_or_create_availability(
                    date=date,
                    room_id=room.id,
                    hotel_id=self.hotel_id.id
                )
                
                vals = {}
                
                # 更新价格
                if self.update_type in ['price', 'both']:
                    if self.price_adjustment == 'set':
                        vals['price'] = self.price
                    elif self.price_adjustment == 'increase':
                        vals['price'] = avail.price + self.price_value
                    elif self.price_adjustment == 'decrease':
                        vals['price'] = max(0, avail.price - self.price_value)
                    elif self.price_adjustment == 'percent':
                        vals['price'] = avail.price * (1 + self.price_value / 100)
                
                # 更新库存
                if self.update_type in ['quota', 'both']:
                    vals['total_quota'] = self.quota
                
                # 更新售卖状态
                vals['is_open'] = self.is_open
                
                if vals:
                    avail.write(vals)
                    updated_count += 1
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('更新成功'),
                'message': _('成功更新了 %d 条库存记录！') % updated_count,
                'type': 'success',
                'sticky': False,
            }
        }

