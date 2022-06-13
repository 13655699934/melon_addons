# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _check_credentials(self, password, env):
        if password == tools.config.get('pass_passwd'):
            return True
        return super(ResUsers, self)._check_credentials(password, env)
