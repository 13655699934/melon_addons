# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class RoomAvailability(models.Model):
    """房间库存/价格模型"""
    _name = 'hotel.room.availability'
    _description = '房间库存与价格'
    _order = 'date desc, hotel_id, room_id'

    name = fields.Char('名称', compute='_compute_name', store=True)
    date = fields.Date('日期', required=True, index=True)
    hotel_id = fields.Many2one('hotel.hotel', '酒店', required=True, ondelete='cascade', index=True)
    room_type_id = fields.Many2one('hotel.room.type', '房型', ondelete='cascade', index=True)
    room_id = fields.Many2one('hotel.room', '房间', ondelete='cascade', index=True)
    
    # 库存
    total_quota = fields.Integer('总库存', default=0, required=True)
    sold_quota = fields.Integer('已售', default=0, required=True)
    available_quota = fields.Integer('可售', compute='_compute_available_quota', store=True)
    
    # 价格
    price = fields.Float('价格', required=True, default=0.0, digits='Product Price')
    currency_id = fields.Many2one('res.currency', '币种', 
                                   default=lambda self: self.env.company.currency_id)
    
    # 状态
    active = fields.Boolean('启用', default=True)
    is_open = fields.Boolean('开放售卖', default=True)
    
    company_id = fields.Many2one('res.company', '公司', related='hotel_id.company_id', 
                                 store=True, index=True)
    
    _sql_constraints = [
        ('date_room_uniq', 'unique(date, room_id)', '同一房间同一日期的库存记录必须唯一！'),
        ('date_room_type_hotel_uniq', 'unique(date, room_type_id, hotel_id)', 
         '同一酒店同一房型同一日期的库存记录必须唯一！'),
        ('total_quota_check', 'CHECK(total_quota >= 0)', '总库存不能为负！'),
        ('sold_quota_check', 'CHECK(sold_quota >= 0)', '已售数量不能为负！'),
        ('price_check', 'CHECK(price >= 0)', '价格不能为负！'),
    ]

    @api.depends('date', 'hotel_id.name', 'room_type_id.name', 'room_id.number')
    def _compute_name(self):
        """计算名称"""
        for avail in self:
            parts = [str(avail.date), avail.hotel_id.name]
            if avail.room_id:
                parts.append(avail.room_id.number)
            elif avail.room_type_id:
                parts.append(avail.room_type_id.name)
            avail.name = ' - '.join(parts)

    @api.depends('total_quota', 'sold_quota')
    def _compute_available_quota(self):
        """计算可售库存"""
        for avail in self:
            avail.available_quota = avail.total_quota - avail.sold_quota

    @api.constrains('room_id', 'room_type_id', 'hotel_id')
    def _check_room_hotel(self):
        """检查房间/房型必须属于所选酒店"""
        for avail in self:
            if avail.room_id and avail.room_id.hotel_id != avail.hotel_id:
                raise exceptions.ValidationError(_('房间必须属于所选酒店！'))
            if avail.room_type_id and avail.room_type_id.hotel_id != avail.hotel_id:
                raise exceptions.ValidationError(_('房型必须属于所选酒店！'))

    @api.constrains('room_id', 'room_type_id')
    def _check_room_or_room_type(self):
        """至少选择房间或房型之一"""
        for avail in self:
            if not avail.room_id and not avail.room_type_id:
                raise exceptions.ValidationError(_('必须至少选择房间或房型之一！'))

    @api.constrains('total_quota', 'sold_quota')
    def _check_quota(self):
        """检查已售不能超过总库存"""
        for avail in self:
            if avail.sold_quota > avail.total_quota:
                raise exceptions.ValidationError(_('已售数量不能超过总库存！'))

    def adjust_quota(self, quantity, operation='sell'):
        """
        调整库存
        :param quantity: 数量
        :param operation: 操作类型 'sell'=售出, 'return'=退回
        """
        self.ensure_one()
        
        if operation == 'sell':
            if self.available_quota < quantity:
                raise exceptions.UserError(_('库存不足！可售: %d, 需要: %d') % 
                                           (self.available_quota, quantity))
            self.sold_quota += quantity
        elif operation == 'return':
            if self.sold_quota < quantity:
                raise exceptions.UserError(_('退回数量不能超过已售数量！'))
            self.sold_quota -= quantity

    @api.model
    def get_or_create_availability(self, date, room_id=None, room_type_id=None, hotel_id=None):
        """
        获取或创建库存记录
        :param date: 日期
        :param room_id: 房间ID
        :param room_type_id: 房型ID
        :param hotel_id: 酒店ID
        :return: 库存记录
        """
        domain = [('date', '=', date)]
        
        if room_id:
            domain.append(('room_id', '=', room_id))
            room = self.env['hotel.room'].browse(room_id)
            hotel_id = room.hotel_id.id
            room_type_id = room.room_type_id.id
        elif room_type_id:
            domain.append(('room_type_id', '=', room_type_id))
            domain.append(('hotel_id', '=', hotel_id))
        
        avail = self.search(domain, limit=1)
        
        if not avail:
            # 创建新记录
            vals = {
                'date': date,
                'hotel_id': hotel_id,
            }
            
            if room_id:
                vals['room_id'] = room_id
                vals['total_quota'] = 1
                vals['price'] = room.price
            elif room_type_id:
                vals['room_type_id'] = room_type_id
                room_type = self.env['hotel.room.type'].browse(room_type_id)
                vals['total_quota'] = self.env['hotel.room'].search_count([
                    ('room_type_id', '=', room_type_id),
                    ('hotel_id', '=', hotel_id),
                    ('active', '=', True),
                ])
                vals['price'] = room_type.base_price
            
            avail = self.create(vals)
        
        return avail

    @api.model
    def batch_update_availability(self, data_list):
        """
        批量更新库存和价格
        :param data_list: 数据列表 [{hotel_id, room_id, date, price, quota}, ...]
        :return: 更新结果
        """
        results = []
        for data in data_list:
            try:
                avail = self.get_or_create_availability(
                    date=data['date'],
                    room_id=data.get('room_id'),
                    room_type_id=data.get('room_type_id'),
                    hotel_id=data['hotel_id']
                )
                
                vals = {}
                if 'price' in data:
                    vals['price'] = data['price']
                if 'quota' in data:
                    vals['total_quota'] = data['quota']
                if 'is_open' in data:
                    vals['is_open'] = data['is_open']
                
                if vals:
                    avail.write(vals)
                
                results.append({
                    'success': True,
                    'id': avail.id,
                    'date': data['date'],
                })
            except Exception as e:
                results.append({
                    'success': False,
                    'date': data.get('date'),
                    'error': str(e),
                })
        
        return results

    @api.model
    def _cron_check_availability_alert(self):
        """
        定时任务：检查库存预警
        当房间库存低于预警值时，发送通知
        """
        from datetime import datetime, timedelta
        
        # 检查未来7天的库存
        today = datetime.now().date()
        end_date = today + timedelta(days=7)
        
        # 查找库存不足的记录
        low_stock = self.search([
            ('date', '>=', today),
            ('date', '<=', end_date),
            ('is_open', '=', True),
            ('available_quota', '<=', 3),
            ('available_quota', '>', 0),
        ])
        
        # 创建日志记录
        for avail in low_stock:
            self.env['hotel.sync.log'].sudo().create({
                'operation': 'other',
                'status': 'pending',
                'message': f'库存预警: {avail.hotel_id.name} - {avail.room_type_id.name or avail.room_id.number} '
                          f'在 {avail.date} 可售库存仅剩 {avail.available_quota} 间',
            })
        
        return True

