# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError, ValidationError


class HotelOrder(models.Model):
    """酒店订单模型"""
    _name = 'hotel.order'
    _description = '酒店订单'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char('订单号', required=True, copy=False, readonly=True,
                       default='New', index=True)
    
    # 渠道与来源
    channel_id = fields.Many2one('hotel.channel', '销售渠道', tracking=True, index=True,
                                  help='为空表示线下订单')
    channel_order_no = fields.Char('渠道订单号', copy=False, index=True)
    source = fields.Selection([
        ('offline', '线下'),
        ('online', '线上'),
    ], string='订单来源', compute='_compute_source', store=True)
    
    # 酒店与房间
    hotel_id = fields.Many2one('hotel.hotel', '酒店', required=True, ondelete='restrict',
                               tracking=True, index=True)
    room_type_id = fields.Many2one('hotel.room.type', '房型', tracking=True, index=True)
    room_id = fields.Many2one('hotel.room', '房间', tracking=True, index=True)
    
    # 预订人信息
    partner_id = fields.Many2one('res.partner', '下单人')
    guest_name = fields.Char('预订人姓名', required=True, tracking=True)
    guest_phone = fields.Char('手机号', required=True, tracking=True)
    guest_email = fields.Char('邮箱')
    guest_id_number = fields.Char('身份证号')
    
    # 日期与间夜
    check_in = fields.Date('入住日期', required=True, tracking=True, index=True)
    check_out = fields.Date('离店日期', required=True, tracking=True, index=True)
    nights = fields.Integer('间夜数', compute='_compute_nights', store=True)
    
    # 数量与价格
    quantity = fields.Integer('房间数量', default=1, required=True, tracking=True)
    unit_price = fields.Float('单价', required=True, digits='Product Price', tracking=True)
    total_price = fields.Float('总价', compute='_compute_total_price', store=True, 
                                digits='Product Price', tracking=True)
    currency_id = fields.Many2one('res.currency', '币种', 
                                   default=lambda self: self.env.company.currency_id)
    
    # 状态
    state = fields.Selection([
        ('draft', '草稿'),
        ('confirmed', '已确认'),
        ('checked_in', '已入住'),
        ('checked_out', '已退房'),
        ('cancelled', '已取消'),
    ], string='状态', default='draft', required=True, tracking=True, index=True)
    
    # 备注
    note = fields.Text('备注')
    cancel_reason = fields.Text('取消原因')
    
    # 时间戳
    confirmed_date = fields.Datetime('确认时间', readonly=True)
    checkin_date = fields.Datetime('入住时间', readonly=True)
    checkout_date = fields.Datetime('退房时间', readonly=True)
    cancelled_date = fields.Datetime('取消时间', readonly=True)
    
    company_id = fields.Many2one('res.company', '公司', related='hotel_id.company_id', 
                                 store=True, index=True)
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', '订单号必须唯一！'),
        ('quantity_check', 'CHECK(quantity > 0)', '房间数量必须大于0！'),
        ('unit_price_check', 'CHECK(unit_price >= 0)', '单价不能为负！'),
    ]

    @api.depends('channel_id')
    def _compute_source(self):
        """计算订单来源"""
        for order in self:
            order.source = 'online' if order.channel_id else 'offline'

    @api.depends('check_in', 'check_out')
    def _compute_nights(self):
        """计算间夜数"""
        for order in self:
            if order.check_in and order.check_out:
                delta = order.check_out - order.check_in
                order.nights = delta.days
            else:
                order.nights = 0

    @api.depends('unit_price', 'quantity', 'nights')
    def _compute_total_price(self):
        """计算总价"""
        for order in self:
            order.total_price = order.unit_price * order.quantity * order.nights

    @api.constrains('check_in', 'check_out')
    def _check_dates(self):
        """检查日期合法性"""
        for order in self:
            if order.check_in and order.check_out:
                if order.check_out <= order.check_in:
                    raise ValidationError(_('离店日期必须晚于入住日期！'))
                if order.check_in < fields.Date.today() and order.state == 'draft':
                    raise ValidationError(_('入住日期不能早于今天！'))

    @api.constrains('hotel_id', 'room_type_id', 'room_id')
    def _check_hotel_consistency(self):
        """检查酒店一致性"""
        for order in self:
            if order.room_id and order.room_id.hotel_id != order.hotel_id:
                raise ValidationError(_('房间必须属于所选酒店！'))
            if order.room_type_id and order.room_type_id.hotel_id != order.hotel_id:
                raise ValidationError(_('房型必须属于所选酒店！'))

    @api.constrains('room_id', 'room_type_id')
    def _check_room_or_room_type(self):
        """至少选择房间或房型之一"""
        for order in self:
            if not order.room_id and not order.room_type_id:
                raise ValidationError(_('必须至少选择房间或房型之一！'))

    @api.model
    def create(self, vals):
        """创建订单时生成订单号"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.order') or 'New'
        return super().create(vals)

    def action_confirm(self):
        """确认订单 - 扣减库存"""
        for order in self:
            if order.state != 'draft':
                raise UserError(_('只能确认草稿状态的订单！'))
            
            # 检查库存
            if order.room_id:
                if not order.room_id.check_availability(order.check_in, order.check_out):
                    raise UserError(_('房间 %s 在所选日期不可用！') % order.room_id.number)
                
                # 更新房间状态
                order.room_id.write({'status': 'reserved'})
            
            # TODO: 扣减库存（hotel.room.availability）
            
            order.write({
                'state': 'confirmed',
                'confirmed_date': fields.Datetime.now(),
            })
            
            # 记录日志
            self.env['hotel.sync.log'].create({
                'channel_id': order.channel_id.id if order.channel_id else False,
                'operation': 'order_confirm',
                'order_id': order.id,
                'status': 'success',
                'message': f'订单 {order.name} 已确认',
            })

    def action_checkin(self):
        """入住"""
        for order in self:
            if order.state != 'confirmed':
                raise UserError(_('只能办理已确认的订单入住！'))
            
            if order.room_id:
                order.room_id.write({'status': 'occupied'})
            
            order.write({
                'state': 'checked_in',
                'checkin_date': fields.Datetime.now(),
            })

    def action_checkout(self):
        """退房"""
        for order in self:
            if order.state != 'checked_in':
                raise UserError(_('只能办理已入住的订单退房！'))
            
            if order.room_id:
                order.room_id.write({'status': 'vacant'})
            
            order.write({
                'state': 'checked_out',
                'checkout_date': fields.Datetime.now(),
            })

    def action_cancel(self):
        """取消订单 - 释放库存"""
        for order in self:
            if order.state not in ['draft', 'confirmed']:
                raise UserError(_('只能取消草稿或已确认的订单！'))
            
            # 释放房间
            if order.room_id and order.room_id.status == 'reserved':
                order.room_id.write({'status': 'vacant'})
            
            # TODO: 释放库存（hotel.room.availability）
            
            order.write({
                'state': 'cancelled',
                'cancelled_date': fields.Datetime.now(),
            })
            
            # 记录日志
            self.env['hotel.sync.log'].create({
                'channel_id': order.channel_id.id if order.channel_id else False,
                'operation': 'order_cancel',
                'order_id': order.id,
                'status': 'success',
                'message': f'订单 {order.name} 已取消',
            })

    def action_clone_book(self):
        """一键复刻下单"""
        self.ensure_one()
        
        # 复制关键字段
        new_order = self.copy({
            'name': 'New',
            'state': 'draft',
            'channel_order_no': False,
            'confirmed_date': False,
            'checkin_date': False,
            'checkout_date': False,
            'cancelled_date': False,
            'cancel_reason': False,
            'note': f'克隆自订单: {self.name}',
        })
        
        # 打开新订单
        return {
            'name': '新订单',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.order',
            'res_id': new_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.onchange('room_id')
    def _onchange_room_id(self):
        """房间变更时同步酒店、房型和价格"""
        if self.room_id:
            self.hotel_id = self.room_id.hotel_id
            self.room_type_id = self.room_id.room_type_id
            self.unit_price = self.room_id.price

    @api.onchange('room_type_id')
    def _onchange_room_type_id(self):
        """房型变更时同步酒店和价格"""
        if self.room_type_id and not self.room_id:
            self.hotel_id = self.room_type_id.hotel_id
            self.unit_price = self.room_type_id.base_price

    def write(self, vals):
        """写入时的权限控制"""
        # 前台用户不能修改价格（需要在安全规则中配置）
        if 'unit_price' in vals or 'total_price' in vals:
            if not self.env.user.has_group('hotel_channel_hub.group_hotel_manager'):
                if not self.env.user.has_group('base.group_system'):
                    raise UserError(_('您没有权限修改订单价格！'))
        
        return super().write(vals)

