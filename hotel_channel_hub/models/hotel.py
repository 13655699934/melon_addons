# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Hotel(models.Model):
    """酒店模型"""
    _name = 'hotel.hotel'
    _description = '酒店'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('酒店名称', required=True, tracking=True)
    code = fields.Char('酒店编码', required=True, copy=False, index=True)
    company_id = fields.Many2one('res.company', '公司', default=lambda self: self.env.company)
    
    # 地址信息
    address = fields.Char('地址', tracking=True)
    city = fields.Char('城市')
    state = fields.Char('省份')
    zip_code = fields.Char('邮编')
    country_id = fields.Many2one('res.country', '国家')
    latitude = fields.Float('纬度', digits=(10, 6))
    longitude = fields.Float('经度', digits=(10, 6))
    
    # 联系信息
    contact_name = fields.Char('联系人')
    phone = fields.Char('电话')
    email = fields.Char('邮箱')
    
    # 业务信息
    active = fields.Boolean('启用', default=True)
    opening_date = fields.Date('入驻时间')
    star_rating = fields.Selection([
        ('1', '一星'),
        ('2', '二星'),
        ('3', '三星'),
        ('4', '四星'),
        ('5', '五星'),
    ], string='星级')
    
    # 图片
    image_1920 = fields.Image('酒店图片', max_width=1920, max_height=1920)
    image_128 = fields.Image('图片缩略图', related='image_1920', max_width=128, max_height=128, store=True)
    
    # 统计字段
    room_count = fields.Integer('房间数', compute='_compute_room_count', store=True)
    room_type_count = fields.Integer('房型数', compute='_compute_room_type_count', store=True)
    order_count = fields.Integer('订单数', compute='_compute_order_count')
    
    # 关联字段
    room_ids = fields.One2many('hotel.room', 'hotel_id', '房间')
    room_type_ids = fields.One2many('hotel.room.type', 'hotel_id', '房型')
    
    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id)', '同一公司下酒店编码必须唯一！'),
    ]

    @api.depends('room_ids')
    def _compute_room_count(self):
        """计算房间数量"""
        for hotel in self:
            hotel.room_count = len(hotel.room_ids)

    @api.depends('room_type_ids')
    def _compute_room_type_count(self):
        """计算房型数量"""
        for hotel in self:
            hotel.room_type_count = len(hotel.room_type_ids)

    def _compute_order_count(self):
        """计算订单数量"""
        for hotel in self:
            hotel.order_count = self.env['hotel.order'].search_count([('hotel_id', '=', hotel.id)])

    def action_view_rooms(self):
        """查看房间"""
        self.ensure_one()
        return {
            'name': '房间列表',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.room',
            'view_mode': 'list,form',
            'domain': [('hotel_id', '=', self.id)],
            'context': {'default_hotel_id': self.id}
        }

    def action_view_orders(self):
        """查看订单"""
        self.ensure_one()
        return {
            'name': '订单列表',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.order',
            'view_mode': 'list,form,calendar',
            'domain': [('hotel_id', '=', self.id)],
            'context': {'default_hotel_id': self.id}
        }

