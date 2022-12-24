# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AuditIpWhitelist(models.Model):
    _name = "audit.ip.whitelist"
    _description = "白名单"
    _order = 'id desc'

    name = fields.Char(string='IP', index=True)
    date = fields.Datetime(string='登陆时间', required=True, readonly=True, index=True, default=fields.Datetime.now)
    state = fields.Selection([
        ('放行', '放行'),
        ('拒绝', '拒绝'),
    ], '状态', readonly=True, copy=False, default='放行')

    audit_login_ids = fields.One2many('audit.login', compute='_compute_audit_login_ids', string='登陆日志', copy=False)

    @api.depends()
    def _compute_audit_login_ids(self):
        for order in self:
            order.audit_login_ids = self.env['audit.login'].sudo().search([('ip', '=', order.name)])

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'IP必须唯一!'),
    ]

    def button_state(self):
        """
        状态变更
        """
        context = dict(self._context or {})
        self.state = context['default_state']
        return True

    def white_ip(self, request):
        """
        IP是否禁用
        :param request:
        :param uid:
        :return:
        """
        values = {}
        environ = request.httprequest.headers.environ
        ip = environ.get("REMOTE_ADDR")
        domain = [('name', '=', ip), ('state', '=', '拒绝')]
        rows_count = request.env['audit.ip.whitelist'].sudo().search_count(domain)
        if rows_count > 0:
            values['error'] = '黑名单用户禁止登陆'
            request.env['audit.login'].add_log(request, False, values)  # 写登陆错误日志
            return False
        return True
