# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta


class TestHotelBasic(TransactionCase):
    """酒店管理基础测试"""

    def setUp(self):
        super().setUp()
        
        # 创建测试酒店
        self.hotel = self.env['hotel.hotel'].create({
            'name': '测试酒店',
            'code': 'TEST001',
            'address': '测试地址',
            'city': '测试城市',
            'phone': '010-12345678',
        })
        
        # 创建测试房型
        self.room_type = self.env['hotel.room.type'].create({
            'name': '测试房型',
            'code': 'RT001',
            'hotel_id': self.hotel.id,
            'bed_type': 'king',
            'max_occupancy': 2,
            'base_price': 500.0,
        })
        
        # 创建测试房间
        self.room = self.env['hotel.room'].create({
            'number': '101',
            'hotel_id': self.hotel.id,
            'room_type_id': self.room_type.id,
            'floor': 1,
            'price': 500.0,
            'status': 'vacant',
        })
        
        # 创建测试渠道
        self.channel = self.env['hotel.channel'].create({
            'name': '测试渠道',
            'code': 'CH001',
            'enterprise_key': 'TEST_ENTERPRISE_001',
        })

    def test_01_hotel_creation(self):
        """测试酒店创建"""
        self.assertTrue(self.hotel.exists())
        self.assertEqual(self.hotel.name, '测试酒店')
        self.assertEqual(self.hotel.code, 'TEST001')

    def test_02_room_type_creation(self):
        """测试房型创建"""
        self.assertTrue(self.room_type.exists())
        self.assertEqual(self.room_type.hotel_id, self.hotel)
        self.assertEqual(self.room_type.base_price, 500.0)

    def test_03_room_creation(self):
        """测试房间创建"""
        self.assertTrue(self.room.exists())
        self.assertEqual(self.room.hotel_id, self.hotel)
        self.assertEqual(self.room.room_type_id, self.room_type)
        self.assertEqual(self.room.status, 'vacant')

    def test_04_channel_token_generation(self):
        """测试渠道Token生成"""
        self.assertTrue(self.channel.token)
        self.assertTrue(self.channel.token_expiry)
        
        # 测试Token轮换
        old_token = self.channel.token
        self.channel.action_generate_token()
        self.assertNotEqual(self.channel.token, old_token)

    def test_05_order_creation(self):
        """测试订单创建"""
        check_in = datetime.now().date() + timedelta(days=1)
        check_out = check_in + timedelta(days=2)
        
        order = self.env['hotel.order'].create({
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'room_type_id': self.room_type.id,
            'guest_name': '测试客人',
            'guest_phone': '13800138000',
            'check_in': check_in,
            'check_out': check_out,
            'quantity': 1,
            'unit_price': 500.0,
        })
        
        self.assertTrue(order.exists())
        self.assertEqual(order.state, 'draft')
        self.assertEqual(order.nights, 2)
        self.assertEqual(order.total_price, 1000.0)

    def test_06_order_confirm(self):
        """测试订单确认流程"""
        check_in = datetime.now().date() + timedelta(days=1)
        check_out = check_in + timedelta(days=2)
        
        order = self.env['hotel.order'].create({
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'room_type_id': self.room_type.id,
            'guest_name': '测试客人',
            'guest_phone': '13800138000',
            'check_in': check_in,
            'check_out': check_out,
            'quantity': 1,
            'unit_price': 500.0,
        })
        
        # 确认订单
        order.action_confirm()
        self.assertEqual(order.state, 'confirmed')
        self.assertTrue(order.confirmed_date)
        
        # 检查房间状态变化
        self.assertEqual(self.room.status, 'reserved')

    def test_07_order_checkin_checkout(self):
        """测试入住和退房流程"""
        check_in = datetime.now().date() + timedelta(days=1)
        check_out = check_in + timedelta(days=2)
        
        order = self.env['hotel.order'].create({
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'room_type_id': self.room_type.id,
            'guest_name': '测试客人',
            'guest_phone': '13800138000',
            'check_in': check_in,
            'check_out': check_out,
            'quantity': 1,
            'unit_price': 500.0,
        })
        
        # 确认订单
        order.action_confirm()
        
        # 入住
        order.action_checkin()
        self.assertEqual(order.state, 'checked_in')
        self.assertEqual(self.room.status, 'occupied')
        
        # 退房
        order.action_checkout()
        self.assertEqual(order.state, 'checked_out')
        self.assertEqual(self.room.status, 'vacant')

    def test_08_order_cancel(self):
        """测试订单取消"""
        check_in = datetime.now().date() + timedelta(days=1)
        check_out = check_in + timedelta(days=2)
        
        order = self.env['hotel.order'].create({
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'room_type_id': self.room_type.id,
            'guest_name': '测试客人',
            'guest_phone': '13800138000',
            'check_in': check_in,
            'check_out': check_out,
            'quantity': 1,
            'unit_price': 500.0,
        })
        
        # 确认订单
        order.action_confirm()
        self.assertEqual(self.room.status, 'reserved')
        
        # 取消订单
        order.action_cancel()
        self.assertEqual(order.state, 'cancelled')
        
        # 检查房间状态恢复
        self.assertEqual(self.room.status, 'vacant')

    def test_09_date_validation(self):
        """测试日期验证"""
        check_in = datetime.now().date() + timedelta(days=2)
        check_out = check_in - timedelta(days=1)  # 错误的日期
        
        with self.assertRaises(ValidationError):
            self.env['hotel.order'].create({
                'hotel_id': self.hotel.id,
                'room_id': self.room.id,
                'room_type_id': self.room_type.id,
                'guest_name': '测试客人',
                'guest_phone': '13800138000',
                'check_in': check_in,
                'check_out': check_out,
                'quantity': 1,
                'unit_price': 500.0,
            })

    def test_10_room_availability(self):
        """测试房间可用性检查"""
        check_in = datetime.now().date() + timedelta(days=1)
        check_out = check_in + timedelta(days=2)
        
        # 创建并确认第一个订单
        order1 = self.env['hotel.order'].create({
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'room_type_id': self.room_type.id,
            'guest_name': '测试客人1',
            'guest_phone': '13800138000',
            'check_in': check_in,
            'check_out': check_out,
            'quantity': 1,
            'unit_price': 500.0,
        })
        order1.action_confirm()
        
        # 检查房间不可用
        is_available = self.room.check_availability(check_in, check_out)
        self.assertFalse(is_available)

    def test_11_availability_model(self):
        """测试库存模型"""
        date = datetime.now().date() + timedelta(days=1)
        
        # 创建库存记录
        avail = self.env['hotel.room.availability'].create({
            'date': date,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'total_quota': 10,
            'sold_quota': 3,
            'price': 500.0,
        })
        
        self.assertEqual(avail.available_quota, 7)
        
        # 测试库存调整
        avail.adjust_quota(2, 'sell')
        self.assertEqual(avail.sold_quota, 5)
        self.assertEqual(avail.available_quota, 5)
        
        # 测试退回库存
        avail.adjust_quota(1, 'return')
        self.assertEqual(avail.sold_quota, 4)
        self.assertEqual(avail.available_quota, 6)

    def test_12_sync_log(self):
        """测试同步日志"""
        log = self.env['hotel.sync.log'].log_api_call(
            operation='order_create',
            channel_id=self.channel.id,
            status='success',
            message='测试日志',
            request_data={'test': 'data'},
            response_data={'result': 'ok'},
            duration=0.5,
        )
        
        self.assertTrue(log.exists())
        self.assertEqual(log.operation, 'order_create')
        self.assertEqual(log.status, 'success')
        self.assertTrue(log.request_data)

    def test_13_order_clone(self):
        """测试订单克隆功能"""
        check_in = datetime.now().date() + timedelta(days=1)
        check_out = check_in + timedelta(days=2)
        
        order1 = self.env['hotel.order'].create({
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'room_type_id': self.room_type.id,
            'guest_name': '测试客人',
            'guest_phone': '13800138000',
            'check_in': check_in,
            'check_out': check_out,
            'quantity': 1,
            'unit_price': 500.0,
        })
        
        # 克隆订单
        result = order1.action_clone_book()
        
        # 验证返回了新订单的动作
        self.assertEqual(result['res_model'], 'hotel.order')
        self.assertTrue(result.get('res_id'))

    def test_14_channel_mapping(self):
        """测试渠道映射"""
        mapping = self.env['hotel.channel.mapping'].create({
            'channel_id': self.channel.id,
            'hotel_id': self.hotel.id,
            'room_type_id': self.room_type.id,
            'channel_product_id': 'CHANNEL_PRODUCT_001',
            'pricing_strategy': 'markup',
            'price_adjustment': 50.0,
        })
        
        # 测试价格计算
        channel_price = mapping.get_channel_price(500.0)
        self.assertEqual(channel_price, 550.0)

    def test_15_permission_check(self):
        """测试权限控制（简单测试）"""
        # 创建普通用户组
        user = self.env['res.users'].create({
            'name': '测试前台用户',
            'login': 'front_desk_test',
            'groups_id': [(4, self.env.ref('hotel_channel_hub.group_front_desk_user').id)],
        })
        
        # 测试前台用户可以查看订单
        order = self.env['hotel.order'].with_user(user).search([('hotel_id', '=', self.hotel.id)])
        self.assertTrue(len(order) >= 0)  # 不报错即可


class TestHotelAPI(TransactionCase):
    """API接口测试（基础）"""

    def setUp(self):
        super().setUp()
        
        self.hotel = self.env['hotel.hotel'].create({
            'name': 'API测试酒店',
            'code': 'API001',
        })
        
        self.room_type = self.env['hotel.room.type'].create({
            'name': 'API测试房型',
            'code': 'RT001',
            'hotel_id': self.hotel.id,
            'bed_type': 'king',
            'max_occupancy': 2,
            'base_price': 600.0,
        })
        
        self.room = self.env['hotel.room'].create({
            'number': '201',
            'hotel_id': self.hotel.id,
            'room_type_id': self.room_type.id,
            'floor': 2,
            'price': 600.0,
            'status': 'vacant',
        })
        
        self.channel = self.env['hotel.channel'].create({
            'name': 'API测试渠道',
            'code': 'API_CH001',
            'enterprise_key': 'API_ENTERPRISE_001',
        })

    def test_01_channel_token_validation(self):
        """测试Token验证"""
        # 验证正确的Token
        is_valid = self.channel.validate_token(self.channel.token)
        self.assertTrue(is_valid)
        
        # 验证错误的Token
        is_valid = self.channel.validate_token('WRONG_TOKEN')
        self.assertFalse(is_valid)

    def test_02_get_channel_by_enterprise_key(self):
        """测试通过企业标识获取渠道"""
        channel = self.env['hotel.channel'].get_channel_by_enterprise_key('API_ENTERPRISE_001')
        self.assertEqual(channel, self.channel)
        
        # 测试不存在的企业标识
        channel = self.env['hotel.channel'].get_channel_by_enterprise_key('NOT_EXISTS')
        self.assertFalse(channel)

