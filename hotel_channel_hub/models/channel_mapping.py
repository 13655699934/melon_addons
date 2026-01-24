# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class ChannelMapping(models.Model):
    """渠道映射模型 - 房型/房间与渠道货架映射"""
    _name = 'hotel.channel.mapping'
    _description = '渠道映射'
    _order = 'channel_id, hotel_id'

    name = fields.Char('映射名称', compute='_compute_name', store=True)
    channel_id = fields.Many2one('hotel.channel', '销售渠道', required=True, ondelete='cascade', index=True)
    hotel_id = fields.Many2one('hotel.hotel', '酒店', required=True, ondelete='cascade', index=True)
    room_type_id = fields.Many2one('hotel.room.type', '房型', ondelete='cascade', index=True)
    room_id = fields.Many2one('hotel.room', '房间', ondelete='cascade', index=True)
    
    # 渠道侧信息
    channel_product_id = fields.Char('渠道货品ID', required=True, 
                                      help='渠道平台的商品/房型ID')
    channel_room_type_id = fields.Char('渠道房型ID')
    
    # 定价策略
    pricing_strategy = fields.Selection([
        ('base', '使用基础价'),
        ('markup', '加价'),
        ('discount', '减价'),
        ('fixed', '固定价'),
    ], string='定价策略', default='base', required=True)
    
    price_adjustment = fields.Float('价格调整', default=0.0, 
                                     help='加价/减价金额，或固定价格')
    price_adjustment_percent = fields.Float('价格调整比例(%)', default=0.0,
                                             help='百分比调整，仅用于加价/减价策略')
    
    # 状态
    active = fields.Boolean('启用', default=True)
    
    company_id = fields.Many2one('res.company', '公司', related='hotel_id.company_id', store=True)
    
    _sql_constraints = [
        ('channel_room_uniq', 'unique(channel_id, room_id)', 
         '同一渠道下房间映射必须唯一！'),
        ('channel_room_type_uniq', 'unique(channel_id, room_type_id)', 
         '同一渠道下房型映射必须唯一！'),
    ]

    @api.depends('channel_id.name', 'hotel_id.name', 'room_type_id.name', 'room_id.number')
    def _compute_name(self):
        """计算映射名称"""
        for mapping in self:
            parts = [mapping.channel_id.name, mapping.hotel_id.name]
            if mapping.room_type_id:
                parts.append(mapping.room_type_id.name)
            if mapping.room_id:
                parts.append(mapping.room_id.number)
            mapping.name = ' - '.join(parts)

    @api.constrains('room_id', 'room_type_id', 'hotel_id')
    def _check_room_hotel(self):
        """检查房间/房型必须属于所选酒店"""
        for mapping in self:
            if mapping.room_id and mapping.room_id.hotel_id != mapping.hotel_id:
                raise exceptions.ValidationError(_('房间必须属于所选酒店！'))
            if mapping.room_type_id and mapping.room_type_id.hotel_id != mapping.hotel_id:
                raise exceptions.ValidationError(_('房型必须属于所选酒店！'))

    @api.constrains('room_id', 'room_type_id')
    def _check_room_or_room_type(self):
        """至少选择房间或房型之一"""
        for mapping in self:
            if not mapping.room_id and not mapping.room_type_id:
                raise exceptions.ValidationError(_('必须至少选择房间或房型之一！'))

    def get_channel_price(self, base_price):
        """
        根据定价策略计算渠道价格
        :param base_price: 基础价格
        :return: 渠道价格
        """
        self.ensure_one()
        
        if self.pricing_strategy == 'base':
            return base_price
        elif self.pricing_strategy == 'markup':
            if self.price_adjustment_percent > 0:
                return base_price * (1 + self.price_adjustment_percent / 100)
            return base_price + self.price_adjustment
        elif self.pricing_strategy == 'discount':
            if self.price_adjustment_percent > 0:
                return base_price * (1 - self.price_adjustment_percent / 100)
            return base_price - self.price_adjustment
        elif self.pricing_strategy == 'fixed':
            return self.price_adjustment
        
        return base_price

