# -*- coding: utf-8 -*-
from odoo import models, fields, api
import uuid
from odoo.exceptions import UserError, ValidationError


class ApplicationManager(models.Model):
    _name = 'melon.application.manager'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = '应用管理'

    @api.model
    def _default_app_key(self):
        return str(uuid.uuid1()).replace('-', '')

    name = fields.Char(u'应用名称',tracking=True)
    app_image = fields.Image(string='应用图标', attachment=True, help=u'(JPG、PNG，256 * 256px，不超过300KB)')
    image_name = fields.Char(u'图片名称')
    appid = fields.Char(u'APP ID', default=lambda self: str(uuid.uuid1().hex).replace('-', '')[0:16], readonly=True)
    appkey = fields.Char(u'APP Key', default=_default_app_key, readonly=True)
    devlop_platform = fields.Selection([('android', 'Android'), ('ios', 'IOS')], string=u'开发平台', default='android',tracking=True,)
    app_type = fields.Selection([('software', '软件'), ('game', '游戏')], string=u'应用类型', default='software',tracking=True,)
    content_type_id = fields.Many2one('application.content.type', u'内容分类',tracking=True,)
    registration_time = fields.Datetime(string='注册时间',tracking=True,)
    app_description = fields.Text(u'应用描述',tracking=True)

    @api.constrains('app_image')
    def app_image_constrains(self):
        for record in self:
            if record.image_name and record.image_name.split('.')[-1] not in ['png', 'jpg', 'PNG', 'JPG']:
                raise ValidationError('注意：只能上传"png", "jpg" 格式图片')
