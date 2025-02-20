import ast
from odoo.addons.web.controllers.home import Home

import logging
from odoo.exceptions import AccessError

import odoo
import odoo.modules.registry
from odoo import http,_
from odoo.http import request
_logger = logging.getLogger(__name__)

CREDENTIAL_PARAMS = ['login', 'password', 'type']

#----------------------------------------------------------
# odoo Web web Controllers
#----------------------------------------------------------
class AuditLogin(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        if request.httprequest.method == 'POST':
            # 登录成功
            values = request.params.copy()
            # is_pass = request.env['audit.ip.whitelist'].sudo().white_ip(request)
            # if not is_pass:
            #     # 如果不在白名单中，返回登录失败
            #     values = request.params.copy()
            #     values['error'] = '登录失败，IP不在白名单中！'
            try:
                credential = {key: value for key, value in request.params.items() if key in CREDENTIAL_PARAMS}
                credential.setdefault('type', 'password')
                uid = request.session.authenticate(request.db, credential)
                values['error'] = '登录成功!'
                # # 添加登录日志
                request.env['audit.login'].sudo().add_log(request,request.db, uid, values)
            except odoo.exceptions.AccessDenied as e:
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = '用户账户或密码错误！'
                else:
                    values['error'] = e.args[0]
                # # 添加登录日志
                request.env['audit.login'].sudo().add_log(request,request.db, False, values)
        return super(AuditLogin, self).web_login(redirect, **kw)

