# -*- coding: utf-8 -*-
import datetime
import ipaddress
import logging
import os
import sys

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class AuditLogin(models.Model):
    _name = "audit.login"
    _description = "登录日志"
    _order = 'id desc'
    _log_access = False

    name = fields.Text(string='消息', help='来源设备', required=True, copy=False, index=True, default=lambda self: u'New')
    model_number = fields.Char(string='设备型号', default='')
    ip = fields.Char(string='来源IP', default='')
    website = fields.Char(string='网址', default='')
    databases = fields.Char(string='数据库', default='')
    login = fields.Char(string='登陆用户名', default='')
    date = fields.Datetime(string='登陆时间', required=True, readonly=True, index=True, default=fields.Datetime.now)
    state = fields.Char(string='状态', default='')
    browser = fields.Char(string='浏览器', default='')
    user_id = fields.Many2one('res.users', '登录账号', copy=False)
    error = fields.Text('错误信息')
    loglevel = fields.Selection([
        ('verbose', '详细信息'),
        ('debug', '调试'),
        ('notice', '通知'),
        ('warning', '警告'),
    ], string=u'日志记录等级', default='verbose')

    def add_log(self, request, uid, values):
        """
        登陆时提供的数据
        :param request:请求
        :param uid:用户ID
        :return:True
        """
        zh_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        environ = request.httprequest.headers.environ
        description = "时间:%s\nIP: %s\nUSER_AGENT: %s\nACCEPT_LANGUAGE: %s\nREFERER: %s" % (zh_time,environ.get("REMOTE_ADDR"),
                                                                                           environ.get(
                                                                                               "HTTP_USER_AGENT"),
                                                                                           environ.get(
                                                                                               "HTTP_ACCEPT_LANGUAGE"),
                                                                                           environ.get(
                                                                                               "HTTP_REFERER"))

        ip = environ.get("REMOTE_ADDR")
        print('values', values)
        value = {
            'login': request.params['login'],
            'ip': environ.get("REMOTE_ADDR"),
            'model_number': request.httprequest.user_agent.platform,
            'browser': request.httprequest.user_agent.browser,
            'name': description,
            'error': values.get('error') or ''
        }
        if uid:
            value['user_id'] = uid
            value['state'] = '正常'
            request.env['audit.login'].sudo().create(value)
        else:
            value['state'] = '异常'
            request.env['audit.login'].sudo().create(value)

        return True

    def private_ip(self, ip):
        """
        IP判断未使用，保留函数
        :param ip:IP地址
        :return:
        """
        try:
            # 判断 python 版本
            if sys.version_info[0] == 2:
                return ipaddress.ip_address(ip.strip().decode("utf-8")).is_private
            elif sys.version_info[0] == 3:
                return ipaddress.ip_address(bytes(ip.strip().encode("utf-8"))).is_private
        except Exception as e:
            return False
