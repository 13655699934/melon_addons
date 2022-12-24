import ast
from odoo.addons.web.controllers.main import Home
import logging

import odoo
import odoo.modules.registry
from odoo import http,_
from odoo.http import request
_logger = logging.getLogger(__name__)


#----------------------------------------------------------
# odoo Web web Controllers
#----------------------------------------------------------
class AuditLogin(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        if request.httprequest.method == 'POST':
            # 登录成功
            values = request.params.copy()
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'],
                                                   request.params['password'])
                values['error'] = '登录成功!'
                # # 添加登录日志
                request.env['audit.login'].sudo().add_log(request, uid, values)
            except odoo.exceptions.AccessDenied as e:
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = '用户密码错误！'
                else:
                    values['error'] = e.args[0]
                # # 添加登录日志
                request.env['audit.login'].sudo().add_log(request, False, values)
        return super(AuditLogin, self).web_login(redirect, **kw)

