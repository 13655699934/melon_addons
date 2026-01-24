# -*- coding: utf-8 -*-

import json
import logging
import os
from datetime import datetime, date, timedelta
import time
from datetime import datetime
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError
import odoo
import odoo.modules.registry
_logger = logging.getLogger(__name__)

#::::::::系统缓存 https://blog.csdn.net/u010070526/article/details/85698682
#:::::::::jinja2模板过滤器----结束
from odoo import fields
import jinja2
from odoo.osv import expression

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = jinja2.FileSystemLoader(searchpath=BASE_DIR + "/static/templates/")
env = jinja2.Environment(loader=templateLoader)


class HotelChannelAPIController(http.Controller):
    """酒店渠道API控制器"""

    def _get_response(self, code=0, msg='', data=None):
        """统一响应格式"""
        return {
            'code': code,
            'msg': msg,
            'data': data or {},
            'timestamp': int(time.time()),
        }

    def _validate_token(self, enterprise_key, token):
        """
        验证Token
        :return: channel对象 或 None
        """
        channel = request.env['hotel.channel'].sudo().get_channel_by_enterprise_key(enterprise_key)
        if not channel:
            return None
        
        if not channel.validate_token(token):
            return None
        
        return channel

    def _log_api_call(self, operation, channel_id=None, status='success', 
                      message='', error='', req_data=None, resp_data=None, 
                      duration=0, order_id=None):
        """记录API调用"""
        request.env['hotel.sync.log'].sudo().log_api_call(
            operation=operation,
            channel_id=channel_id,
            status=status,
            message=message,
            error_message=error,
            request_data=req_data,
            response_data=resp_data,
            duration=duration,
            order_id=order_id,
            ip_address=request.httprequest.remote_addr,
        )


    @http.route('/hotel/data/center/index', type='http', auth="none", csrf=False)
    def hotel_data_center_index(self, **kw):
        """
        首页机构数据
        :param model:
        :param id:
        :param kw:
        :return:
        """
        kw.update({"inst": True})
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        user = pool['res.users'].sudo().browse(request.session.uid)
        values = {}
        template = env.get_template('hotel/data_center.html')
        html = template.render(object=values)
        return html

    # ==================== API 1: 获取企业接入Token ====================
    @http.route('/api/channel/token', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_channel_token(self, **kwargs):
        """
        获取或刷新渠道Token
        POST /api/channel/token
        {
            "enterprise_key": "ENTERPRISE_KEY_001"
        }
        """
        start_time = time.time()
        enterprise_key = kwargs.get('enterprise_key')
        
        if not enterprise_key:
            return self._get_response(-1, '缺少企业唯一标识 enterprise_key')
        
        try:
            channel = request.env['hotel.channel'].sudo().get_channel_by_enterprise_key(enterprise_key)
            
            if not channel:
                self._log_api_call('token_get', status='failed', 
                                   message=f'企业标识 {enterprise_key} 不存在',
                                   req_data=kwargs, duration=time.time() - start_time)
                return self._get_response(-1, f'企业标识 {enterprise_key} 不存在')
            
            # 如果Token不存在或已过期，重新生成
            if not channel.token or (channel.token_expiry and channel.token_expiry < datetime.now()):
                channel.action_generate_token()
            
            data = {
                'enterprise_key': channel.enterprise_key,
                'token': channel.token,
                'expiry': channel.token_expiry.strftime('%Y-%m-%d %H:%M:%S') if channel.token_expiry else None,
            }
            
            self._log_api_call('token_get', channel_id=channel.id, status='success',
                               message='Token获取成功', req_data=kwargs, resp_data=data,
                               duration=time.time() - start_time)
            
            return self._get_response(0, 'Token获取成功', data)
        
        except Exception as e:
            _logger.exception('获取Token异常')
            self._log_api_call('token_get', status='failed', error=str(e),
                               req_data=kwargs, duration=time.time() - start_time)
            return self._get_response(-1, f'系统异常: {str(e)}')

    # ==================== API 2: 获取酒店/房型/房间信息 ====================
    @http.route('/api/hotel/rooms', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_hotel_rooms(self, **kwargs):
        """
        获取酒店房间列表
        POST /api/hotel/rooms
        {
            "enterprise_key": "xxx",
            "token": "xxx",
            "hotel_id": 1,
            "page": 1,
            "page_size": 20
        }
        """
        start_time = time.time()
        enterprise_key = kwargs.get('enterprise_key')
        token = kwargs.get('token')
        hotel_id = kwargs.get('hotel_id')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('page_size', 20)
        
        # 验证Token
        channel = self._validate_token(enterprise_key, token)
        if not channel:
            return self._get_response(-1, 'Token验证失败')
        
        try:
            domain = [('active', '=', True)]
            if hotel_id:
                domain.append(('hotel_id', '=', hotel_id))
            
            Room = request.env['hotel.room'].sudo()
            total = Room.search_count(domain)
            rooms = Room.search(domain, offset=(page - 1) * page_size, limit=page_size)
            
            data = {
                'total': total,
                'page': page,
                'page_size': page_size,
                'rooms': [{
                    'id': room.id,
                    'number': room.number,
                    'hotel_id': room.hotel_id.id,
                    'hotel_name': room.hotel_id.name,
                    'room_type_id': room.room_type_id.id,
                    'room_type_name': room.room_type_id.name,
                    'floor': room.floor,
                    'status': room.status,
                    'sale_type': room.sale_type,
                    'price': room.price,
                    'bed_type': room.room_type_id.bed_type,
                    'max_occupancy': room.room_type_id.max_occupancy,
                    'has_breakfast': room.room_type_id.has_breakfast,
                } for room in rooms]
            }
            
            self._log_api_call('room_query', channel_id=channel.id, status='success',
                               message=f'查询到 {len(rooms)} 间房间',
                               req_data=kwargs, resp_data={'total': total},
                               duration=time.time() - start_time)
            
            return self._get_response(0, '查询成功', data)
        
        except Exception as e:
            _logger.exception('查询房间异常')
            self._log_api_call('room_query', channel_id=channel.id, status='failed',
                               error=str(e), req_data=kwargs, duration=time.time() - start_time)
            return self._get_response(-1, f'查询失败: {str(e)}')

    # ==================== API 3: 创建订单 ====================
    @http.route('/api/order/create', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def create_order(self, **kwargs):
        """
        创建订单
        POST /api/order/create
        {
            "enterprise_key": "xxx",
            "token": "xxx",
            "hotel_id": 1,
            "room_id": 10,  // 或 room_type_id
            "check_in": "2025-11-10",
            "check_out": "2025-11-12",
            "quantity": 1,
            "guest_name": "张三",
            "guest_phone": "13800138000",
            "channel_order_no": "CH123456789"
        }
        """
        start_time = time.time()
        enterprise_key = kwargs.get('enterprise_key')
        token = kwargs.get('token')
        
        # 验证Token
        channel = self._validate_token(enterprise_key, token)
        if not channel:
            return self._get_response(-1, 'Token验证失败')
        
        try:
            # 必填字段检查
            required_fields = ['hotel_id', 'check_in', 'check_out', 'guest_name', 'guest_phone']
            for field in required_fields:
                if not kwargs.get(field):
                    return self._get_response(-1, f'缺少必填字段: {field}')
            
            # 至少需要room_id或room_type_id
            if not kwargs.get('room_id') and not kwargs.get('room_type_id'):
                return self._get_response(-1, '必须提供 room_id 或 room_type_id')
            
            # 构建订单数据
            order_vals = {
                'channel_id': channel.id,
                'channel_order_no': kwargs.get('channel_order_no'),
                'hotel_id': kwargs['hotel_id'],
                'room_id': kwargs.get('room_id'),
                'room_type_id': kwargs.get('room_type_id'),
                'check_in': kwargs['check_in'],
                'check_out': kwargs['check_out'],
                'quantity': kwargs.get('quantity', 1),
                'guest_name': kwargs['guest_name'],
                'guest_phone': kwargs['guest_phone'],
                'guest_email': kwargs.get('guest_email'),
                'guest_id_number': kwargs.get('guest_id_number'),
                'note': kwargs.get('note'),
            }
            
            # 获取价格
            if kwargs.get('unit_price'):
                order_vals['unit_price'] = kwargs['unit_price']
            elif kwargs.get('room_id'):
                room = request.env['hotel.room'].sudo().browse(kwargs['room_id'])
                order_vals['unit_price'] = room.price
            elif kwargs.get('room_type_id'):
                room_type = request.env['hotel.room.type'].sudo().browse(kwargs['room_type_id'])
                order_vals['unit_price'] = room_type.base_price
            
            # 创建订单
            order = request.env['hotel.order'].sudo().create(order_vals)
            
            # 自动确认
            if kwargs.get('auto_confirm', True):
                try:
                    order.action_confirm()
                except (ValidationError, UserError) as e:
                    # 如果确认失败，删除订单并返回错误
                    order.unlink()
                    raise e
            
            data = {
                'order_id': order.id,
                'order_no': order.name,
                'state': order.state,
                'total_price': order.total_price,
                'nights': order.nights,
            }
            
            self._log_api_call('order_create', channel_id=channel.id, order_id=order.id,
                               status='success', message=f'订单 {order.name} 创建成功',
                               req_data=kwargs, resp_data=data, duration=time.time() - start_time)
            
            return self._get_response(0, '订单创建成功', data)
        
        except (ValidationError, UserError) as e:
            _logger.warning('创建订单验证失败: %s', str(e))
            self._log_api_call('order_create', channel_id=channel.id, status='failed',
                               error=str(e), req_data=kwargs, duration=time.time() - start_time)
            return self._get_response(-1, f'订单创建失败: {str(e)}')
        
        except Exception as e:
            _logger.exception('创建订单异常')
            self._log_api_call('order_create', channel_id=channel.id, status='failed',
                               error=str(e), req_data=kwargs, duration=time.time() - start_time)
            return self._get_response(-1, f'系统异常: {str(e)}')

    # ==================== API 4: 更新房间（价格/数量）====================
    @http.route('/api/room/update', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def update_room_availability(self, **kwargs):
        """
        批量更新房间价格和库存
        POST /api/room/update
        {
            "enterprise_key": "xxx",
            "token": "xxx",
            "updates": [
                {
                    "hotel_id": 1,
                    "room_id": 10,
                    "date": "2025-11-10",
                    "price": 399,
                    "quota": 3
                }
            ]
        }
        """
        start_time = time.time()
        enterprise_key = kwargs.get('enterprise_key')
        token = kwargs.get('token')
        
        # 验证Token
        channel = self._validate_token(enterprise_key, token)
        if not channel:
            return self._get_response(-1, 'Token验证失败')
        
        try:
            updates = kwargs.get('updates', [])
            if not updates:
                return self._get_response(-1, '缺少更新数据')
            
            # 批量更新
            results = request.env['hotel.room.availability'].sudo().batch_update_availability(updates)
            
            success_count = sum(1 for r in results if r.get('success'))
            
            self._log_api_call('availability_update', channel_id=channel.id, status='success',
                               message=f'成功更新 {success_count}/{len(results)} 条记录',
                               req_data={'count': len(updates)}, resp_data={'results': results},
                               duration=time.time() - start_time)
            
            return self._get_response(0, '更新完成', {'results': results})
        
        except Exception as e:
            _logger.exception('更新库存异常')
            self._log_api_call('availability_update', channel_id=channel.id, status='failed',
                               error=str(e), req_data=kwargs, duration=time.time() - start_time)
            return self._get_response(-1, f'更新失败: {str(e)}')

    # ==================== API 5: 订单更新 ====================
    @http.route('/api/order/update', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def update_order(self, **kwargs):
        """
        更新订单（取消等）
        POST /api/order/update
        {
            "enterprise_key": "xxx",
            "token": "xxx",
            "order_id": 123,  // 或 order_no
            "action": "cancel",  // cancel, update_dates
            "cancel_reason": "客户取消",
            "check_in": "2025-11-11",  // 用于update_dates
            "check_out": "2025-11-13"
        }
        """
        start_time = time.time()
        enterprise_key = kwargs.get('enterprise_key')
        token = kwargs.get('token')
        
        # 验证Token
        channel = self._validate_token(enterprise_key, token)
        if not channel:
            return self._get_response(-1, 'Token验证失败')
        
        try:
            order_id = kwargs.get('order_id')
            order_no = kwargs.get('order_no')
            action = kwargs.get('action')
            
            if not action:
                return self._get_response(-1, '缺少操作类型 action')
            
            # 查找订单
            Order = request.env['hotel.order'].sudo()
            if order_id:
                order = Order.browse(order_id)
            elif order_no:
                order = Order.search([('name', '=', order_no)], limit=1)
            else:
                return self._get_response(-1, '必须提供 order_id 或 order_no')
            
            if not order.exists():
                return self._get_response(-1, '订单不存在')
            
            # 检查订单属于该渠道
            if order.channel_id != channel:
                return self._get_response(-1, '无权操作此订单')
            
            # 执行操作
            if action == 'cancel':
                order.write({'cancel_reason': kwargs.get('cancel_reason', '渠道取消')})
                order.action_cancel()
                message = '订单已取消'
            
            elif action == 'update_dates':
                if not kwargs.get('check_in') or not kwargs.get('check_out'):
                    return self._get_response(-1, '缺少入住或离店日期')
                order.write({
                    'check_in': kwargs['check_in'],
                    'check_out': kwargs['check_out'],
                })
                message = '订单日期已更新'
            
            else:
                return self._get_response(-1, f'不支持的操作: {action}')
            
            data = {
                'order_id': order.id,
                'order_no': order.name,
                'state': order.state,
            }
            
            self._log_api_call('order_update', channel_id=channel.id, order_id=order.id,
                               status='success', message=message,
                               req_data=kwargs, resp_data=data, duration=time.time() - start_time)
            
            return self._get_response(0, message, data)
        
        except (ValidationError, UserError) as e:
            _logger.warning('更新订单验证失败: %s', str(e))
            self._log_api_call('order_update', channel_id=channel.id, status='failed',
                               error=str(e), req_data=kwargs, duration=time.time() - start_time)
            return self._get_response(-1, f'更新失败: {str(e)}')
        
        except Exception as e:
            _logger.exception('更新订单异常')
            self._log_api_call('order_update', channel_id=channel.id, status='failed',
                               error=str(e), req_data=kwargs, duration=time.time() - start_time)
            return self._get_response(-1, f'系统异常: {str(e)}')

    # ==================== API 6: 订单详情 ====================
    @http.route('/api/order/detail', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_order_detail(self, **kwargs):
        """
        获取订单详情
        POST /api/order/detail
        {
            "enterprise_key": "xxx",
            "token": "xxx",
            "order_id": 123  // 或 order_no
        }
        """
        start_time = time.time()
        enterprise_key = kwargs.get('enterprise_key')
        token = kwargs.get('token')
        
        # 验证Token
        channel = self._validate_token(enterprise_key, token)
        if not channel:
            return self._get_response(-1, 'Token验证失败')
        
        try:
            order_id = kwargs.get('order_id')
            order_no = kwargs.get('order_no')
            
            # 查找订单
            Order = request.env['hotel.order'].sudo()
            if order_id:
                order = Order.browse(order_id)
            elif order_no:
                order = Order.search([('name', '=', order_no)], limit=1)
            else:
                return self._get_response(-1, '必须提供 order_id 或 order_no')
            
            if not order.exists():
                return self._get_response(-1, '订单不存在')
            
            # 检查订单属于该渠道（或允许查询所有订单）
            if order.channel_id and order.channel_id != channel:
                return self._get_response(-1, '无权查看此订单')
            
            data = {
                'order_id': order.id,
                'order_no': order.name,
                'channel_order_no': order.channel_order_no,
                'hotel_id': order.hotel_id.id,
                'hotel_name': order.hotel_id.name,
                'room_id': order.room_id.id if order.room_id else None,
                'room_number': order.room_id.number if order.room_id else None,
                'room_type_id': order.room_type_id.id if order.room_type_id else None,
                'room_type_name': order.room_type_id.name if order.room_type_id else None,
                'guest_name': order.guest_name,
                'guest_phone': order.guest_phone,
                'guest_email': order.guest_email,
                'check_in': str(order.check_in),
                'check_out': str(order.check_out),
                'nights': order.nights,
                'quantity': order.quantity,
                'unit_price': order.unit_price,
                'total_price': order.total_price,
                'state': order.state,
                'confirmed_date': order.confirmed_date.strftime('%Y-%m-%d %H:%M:%S') if order.confirmed_date else None,
                'checkin_date': order.checkin_date.strftime('%Y-%m-%d %H:%M:%S') if order.checkin_date else None,
                'checkout_date': order.checkout_date.strftime('%Y-%m-%d %H:%M:%S') if order.checkout_date else None,
                'note': order.note,
            }
            
            self._log_api_call('order_query', channel_id=channel.id, order_id=order.id,
                               status='success', message='订单详情查询成功',
                               req_data=kwargs, duration=time.time() - start_time)
            
            return self._get_response(0, '查询成功', data)
        
        except Exception as e:
            _logger.exception('查询订单详情异常')
            self._log_api_call('order_query', channel_id=channel.id, status='failed',
                               error=str(e), req_data=kwargs, duration=time.time() - start_time)
            return self._get_response(-1, f'查询失败: {str(e)}')

