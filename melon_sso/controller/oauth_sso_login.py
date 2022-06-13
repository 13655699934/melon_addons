# -*- coding: utf-8 -*-
import os
import odoo
from odoo import http, fields, _
from odoo import api, fields, models, _, tools
from odoo.http import request
from jinja2 import Environment, FileSystemLoader
import json
import requests
import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
import logging

_logger = logging.getLogger(__name__)
from odoo.addons.web.controllers.main import db_monodb, ensure_db, set_cookie_and_redirect, login_and_redirect

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


class Home(Home):

    def _login_redirect(self, uid, redirect=None):
        return _get_login_redirect_url(uid, redirect)

    @http.route('/web/oauth/sso', type='http', auth="public", sitemap=False, csrf=False)
    def entrust_oauth_sso_login(self, redirect=None, **kw):
        """
        通过oauth方式调用：
            1、通过授权码获取访问令牌:  {"code":"xxxxxxx","state":"eetrust"}
            2、通过访问令牌获取用户信息: {"code":"xxxxxxx","passport":"test01"}
            3、通过用户信息进行跳转:
                通过：passport是唯一标识
                    redirect_uri 应用跳转路由
                    client_id 应用编码
                    client_secret 应用秘钥
                    eetrust_url   平台url
        :param
        :param redirect:重定向
        :param kw:
        :return:
        """
        ensure_db()
        _logger.info("-------------oauth2.0方式---sso---kw--------------------------:%s", kw)
        param_obj = request.env['ir.config_parameter'].sudo()
        code = kw.get('code')
        redirect_uri = param_obj.get_param('app_redirect_uri') or ''
        client_id = param_obj.get_param('app_client_id') or ''
        client_secret = param_obj.get_param('app_client_secret') or ''
        eetrust_url = param_obj.get_param('eetrust_oauth_url') or ''

        # 获取访问令牌
        token_url = "%s/servlet/oauth/accessToken" % eetrust_url
        header = {
            "accept": "application/json"
        }
        order_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }
        res = requests.post(token_url, data=order_data, headers=header)
        access_token = ""
        if res.status_code == 200:
            res_dict = res.json()
            access_token = res_dict.get("access_token")
        if not access_token:
            return json.dumps({'errmsg': u'1', 'message': u'Access token acquisition failed!'})

        # 获取用户信息
        user_url = "%s/servlet/oauth/userInfo?access_token=%s" % (eetrust_url, access_token)
        headers = {
            'accept': 'application/json',
        }
        res = requests.post(user_url, headers=headers)

        passport = ''
        result_code = ''
        if res.status_code == 200:
            user_info = res.json()
            result_code = user_info.get('code')
            passport = user_info.get('passport')
        if not result_code or result_code == "1":
            return json.dumps({'errmsg': u'1', 'message': u'User information acquisition failed!'})
        id_card = passport
        values = request.params.copy()
        pass_passwd = tools.config.get('pass_passwd')
        # 这里根据最后业务修改
        users = request.env['res.users'].sudo().search([('login', '=', id_card)], order="id desc", limit=1)
        if not users:
            values['error'] = '用户在系统中不存在!'
            # request.env['ir.login'].add_log(request, False, values)  # 写登陆失败日志
            return json.dumps({'errmsg': u'1', 'message': u'System identity account does not exist!'})
        request.params['login'] = users.login
        uid = request.session.authenticate(request.session.db, users.login, pass_passwd)
        # request.env['ir.login'].add_log(request, uid, values)  # 写登陆成功日志
        # return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
        return request.redirect(self._login_redirect(uid, redirect=redirect))

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/page/close'):
        """重写退出登录：SSO不允许登录到系统"""
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect(redirect, 303)

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect='/page/close'):
        """登录界面不允许出现"""
        return werkzeug.utils.redirect(redirect, 303)

    @http.route('/page/close', type='http', auth="none")
    def close_page(self, redirect=None, **kw):
        """关闭页面：存在问题是：会显示空白页"""
        html_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../views/close_page.html'))
        with open(html_path, encoding='utf-8', errors='ignore') as f:
            return f.read()
