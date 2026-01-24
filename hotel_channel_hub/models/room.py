# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class Room(models.Model):
    """房间模型"""
    _name = 'hotel.room'
    _description = '房间'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'hotel_id, floor, number'

    name = fields.Char('房间名称', compute='_compute_name', store=True)
    number = fields.Char('房间号', required=True, index=True, tracking=True)
    hotel_id = fields.Many2one('hotel.hotel', '所属酒店', required=True, ondelete='cascade', index=True)
    room_type_id = fields.Many2one('hotel.room.type', '房型', required=True, ondelete='restrict', index=True)
    company_id = fields.Many2one('res.company', '公司', related='hotel_id.company_id', store=True)
    
    # 房间信息
    floor = fields.Integer('楼层', required=True, default=1)
    status = fields.Selection([
        ('vacant', '空闲'),
        ('reserved', '已预订'),
        ('occupied', '已入住'),
        ('out_of_service', '维修中'),
    ], string='房态', default='vacant', required=True, tracking=True, index=True)
    
    # 售卖设置
    sale_type = fields.Selection([
        ('offline', '仅线下'),
        ('online', '仅线上'),
        ('both', '线上线下'),
    ], string='售卖类型', default='both', required=True)
    
    price = fields.Float('房间价格', required=True, default=0.0, digits='Product Price', tracking=True)
    currency_id = fields.Many2one('res.currency', '币种', 
                                   default=lambda self: self.env.company.currency_id)
    
    # 渠道设置
    min_channel_quota = fields.Integer('渠道最小留量', default=0, 
                                        help='渠道售卖时保留的最小库存量')
    
    # 状态与备注
    active = fields.Boolean('启用', default=True)
    note = fields.Text('备注')
    
    # 统计字段
    order_count = fields.Integer('订单数', compute='_compute_order_count')
    current_order_id = fields.Many2one('hotel.order', '当前订单', compute='_compute_current_order')
    
    _sql_constraints = [
        ('number_hotel_uniq', 'unique(number, hotel_id)', '同一酒店下房间号必须唯一！'),
        ('price_check', 'CHECK(price >= 0)', '房间价格不能为负！'),
        ('min_quota_check', 'CHECK(min_channel_quota >= 0)', '渠道最小留量不能为负！'),
    ]

    @api.depends('number', 'hotel_id.name')
    def _compute_name(self):
        """计算房间完整名称"""
        for room in self:
            if room.hotel_id and room.number:
                room.name = f'{room.hotel_id.name} - {room.number}'
            else:
                room.name = room.number or '/'

    def _compute_order_count(self):
        """计算订单数量"""
        for room in self:
            room.order_count = self.env['hotel.order'].search_count([('room_id', '=', room.id)])

    def _compute_current_order(self):
        """计算当前订单（已预订或已入住的订单）"""
        for room in self:
            order = self.env['hotel.order'].search([
                ('room_id', '=', room.id),
                ('state', 'in', ['confirmed', 'checked_in']),
                ('check_in', '<=', fields.Date.today()),
                ('check_out', '>=', fields.Date.today()),
            ], limit=1, order='check_in desc')
            room.current_order_id = order

    @api.onchange('room_type_id')
    def _onchange_room_type_id(self):
        """房型变更时同步价格"""
        if self.room_type_id:
            self.price = self.room_type_id.base_price

    @api.constrains('hotel_id', 'room_type_id')
    def _check_hotel_room_type(self):
        """检查房型必须属于所选酒店"""
        for room in self:
            if room.room_type_id.hotel_id != room.hotel_id:
                raise exceptions.ValidationError(_('房型必须属于所选酒店！'))

    def action_set_vacant(self):
        """设置为空闲"""
        self.write({'status': 'vacant'})

    def action_set_out_of_service(self):
        """设置为维修中"""
        self.write({'status': 'out_of_service'})

    def action_view_orders(self):
        """查看该房间的所有订单"""
        self.ensure_one()
        return {
            'name': f'{self.name} - 订单列表',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.order',
            'view_mode': 'list,form,calendar',
            'domain': [('room_id', '=', self.id)],
            'context': {'default_room_id': self.id, 'default_hotel_id': self.hotel_id.id}
        }

    def check_availability(self, check_in, check_out):
        """
        检查房间在指定日期范围内是否可用
        :param check_in: 入住日期
        :param check_out: 离店日期
        :return: Boolean
        """
        self.ensure_one()
        
        if self.status == 'out_of_service':
            return False
        
        # 查询是否有冲突的订单
        conflicting_orders = self.env['hotel.order'].search([
            ('room_id', '=', self.id),
            ('state', 'in', ['confirmed', 'checked_in']),
            ('check_in', '<', check_out),
            ('check_out', '>', check_in),
        ])
        
        return not conflicting_orders

