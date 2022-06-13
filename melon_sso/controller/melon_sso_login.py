# -*- coding: utf-8 -*-
import os
import odoo
import requests
from odoo import http, fields, _
from odoo import api, fields, models, _, tools
from odoo.http import request
from jinja2 import Environment, FileSystemLoader
import json
import logging
import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from odoo.addons.web.controllers.main import db_monodb, ensure_db, set_cookie_and_redirect, login_and_redirect

_logger = logging.getLogger(__name__)
#:::访问static静态文件
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/static/templates")
env = Environment(loader=templateLoader)
from odoo.addons.web.controllers.main import WebClient, Home


def _get_login_redirect_url(uid, redirect=None):
    """ Decide if user requires a specific post-login redirect, e.g. for 2FA, or if they are
        fully logged and can proceed to the requested URL
    """
    if request.session.uid:  # fully logged
        return redirect or '/web'

    # partial session (MFA)
    url = request.env(user=uid)['res.users'].browse(uid)._mfa_url()
    if not redirect:
        return url
    parsed = werkzeug.urls.url_parse(url)
    qs = parsed.decode_query()
    qs['redirect'] = redirect
    return parsed.replace(query=werkzeug.urls.url_encode(qs)).to_url()


class MelonHome(Home):

    def _login_redirect(self, uid, redirect=None):
        return _get_login_redirect_url(uid, redirect)

    @http.route('/web/melon/sso', type='http', auth="public", sitemap=False, csrf=False)
    def melon_sso_login(self, redirect=None, **kw):
        """
            xx公司的单点登录原理：
            实现方式1：通过url将用户信息传给应用系统
            {
               '?': '',
               'MELON_CLIENT_IP': '192.168.43.25',
               'MELON_NOT_AFTER': '2025-03-11-15-24-55',
               'MELON_CERT_SERIAL_NUMBER': '6B4C000000000059',
               'MELON_CERT_CN': 'test-17',
               'MELON_CERT_G': '511324199508094736|00',
               'SSL_VERIFY_CERT': 'yes'
             }
            MELON_CERT_G的值截取前18位

            实现方式2：用户信息放在headers里，从cookie里取
                     todo  header1=request.httprequest.headers
                     cookie里面数据格式跟url里一样
                     后面逻辑都一样，不再赘述

          :param redirect:重定向
          :param kw:
          :return:
        """
        ensure_db()
        _logger.info("---------------sso---kw--------------------------:%s", kw)
        cert_g = kw.get('MELON_CERT_G')
        # cookie方式验证
        # cookie = request.httprequest.headers.get("Cookie")
        # cert_g = cookie.get('MELON_CERT_G')
        if not cert_g:
            return json.dumps({'errmsg': u'-1', 'message': u'MELON_CERT_G Value does not exist!'})
        values = request.params.copy()
        # id_card = cert_g[0:18]
        login= cert_g
        pass_passwd = tools.config.get('pass_passwd')
        # 后面新增用户身份证号字段，用来查询
        users = request.env['res.users'].sudo().search([('login', '=', login)], order="id desc", limit=1)
        if not users:
            return json.dumps({'errmsg': u'-1', 'message': u'System identity account does not exist!'})
        uid = request.session.authenticate(request.session.db, users.login, pass_passwd)
        # return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
        return request.redirect(self._login_redirect(uid, redirect=redirect))

    # @http.route('/web/session/logout', type='http', auth="none")
    # def logout(self, redirect='/page/close'):
    #     """重写退出登录：SSO不允许登录到系统"""
    #     request.session.logout(keep_db=True)
    #     return werkzeug.utils.redirect(redirect, 303)
    #
    # @http.route('/web/login', type='http', auth="none")
    # def web_login(self, redirect='/page/close'):
    #     """登录界面不允许出现"""
    #     return werkzeug.utils.redirect(redirect, 303)

    # @http.route('/page/close', type='http', auth="none")
    # def close_page(self, redirect=None, **kw):
    #     """关闭页面：存在问题是：会显示空白页"""
    #     html_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../views/close_page.html'))
    #     with open(html_path, encoding='utf-8', errors='ignore') as f:
    #         return f.read()
