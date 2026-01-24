# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class RoomType(models.Model):
    """房型模型"""
    _name = 'hotel.room.type'
    _description = '房型'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char('房型名称', required=True, tracking=True)
    code = fields.Char('房型编码', required=True, copy=False, index=True)
    hotel_id = fields.Many2one('hotel.hotel', '所属酒店', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', '公司', related='hotel_id.company_id', store=True)
    sequence = fields.Integer('排序', default=10)
    active = fields.Boolean('启用', default=True)
    
    # 房型信息
    bed_type = fields.Selection([
        ('single', '单床'),
        ('double', '双床'),
        ('king', '大床'),
        ('suite', '套房'),
    ], string='床型', default='single', required=True)
    
    max_occupancy = fields.Integer('最多入住人数', default=2, required=True)
    area = fields.Float('面积(㎡)', digits=(8, 2))
    floor_range = fields.Char('楼层范围', help='如: 3-8层')
    
    # 价格与规则
    base_price = fields.Float('基础价格', required=True, default=0.0, digits='Product Price')
    currency_id = fields.Many2one('res.currency', '币种', 
                                   default=lambda self: self.env.company.currency_id)
    
    # 设施与服务
    has_breakfast = fields.Boolean('含早餐', default=False)
    breakfast_count = fields.Integer('早餐份数', default=0)
    has_wifi = fields.Boolean('含WiFi', default=True)
    has_window = fields.Boolean('有窗', default=True)
    
    # 取消规则
    cancellation_policy = fields.Selection([
        ('free', '免费取消'),
        ('1day', '提前1天可取消'),
        ('3day', '提前3天可取消'),
        ('7day', '提前7天可取消'),
        ('no_cancel', '不可取消'),
    ], string='取消规则', default='1day')
    
    # 描述
    description = fields.Text('描述')
    facilities = fields.Text('设施说明')
    
    # 统计
    room_count = fields.Integer('房间数', compute='_compute_room_count', store=True)
    room_ids = fields.One2many('hotel.room', 'room_type_id', '房间')
    
    _sql_constraints = [
        ('code_hotel_uniq', 'unique(code, hotel_id)', '同一酒店下房型编码必须唯一！'),
        ('base_price_check', 'CHECK(base_price >= 0)', '基础价格不能为负！'),
        ('max_occupancy_check', 'CHECK(max_occupancy > 0)', '入住人数必须大于0！'),
    ]

    @api.depends('room_ids')
    def _compute_room_count(self):
        """计算房间数量"""
        for room_type in self:
            room_type.room_count = len(room_type.room_ids)

    @api.onchange('hotel_id')
    def _onchange_hotel_id(self):
        """切换酒店时清空不匹配的数据"""
        if self.hotel_id:
            self.company_id = self.hotel_id.company_id

    def action_view_rooms(self):
        """查看该房型的所有房间"""
        self.ensure_one()
        return {
            'name': f'{self.name} - 房间列表',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.room',
            'view_mode': 'list,form',
            'domain': [('room_type_id', '=', self.id)],
            'context': {
                'default_hotel_id': self.hotel_id.id,
                'default_room_type_id': self.id,
            }
        }

