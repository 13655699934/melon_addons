# -*- coding: utf-8 -*-
from math import floor
import base64
import io
import re
import os
from odoo import models, fields, api
import uuid
import logging
from odoo.exceptions import UserError, ValidationError
import qrcode
from PIL import Image
from io import BytesIO

_logger = logging.getLogger(__name__)


class ApplicationVersion(models.Model):
    _name = 'melon.application.version'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '版本管理'

    @api.depends('qr_code_url')
    def _generate_qr_code(self):
        """根据内容生成二维码，并在二维码中间添加logo"""
        for record in self:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
            qr_code_img = False
            if record.qr_code_url:
                qr.add_data(record.qr_code_url)
                qr.make(fit=True)
                img = qr.make_image()
                img = img.convert("RGBA")
                icon = Image.open(io.BytesIO(base64.b64decode(self.app_id.app_image))).convert("RGBA")
                img_w, img_h = img.size
                factor = 6
                size_w = int(img_w / factor)
                size_h = int(img_h / factor)
                icon_w, icon_h = icon.size
                if icon_w > size_w:
                    icon_w = size_w
                if icon_h > size_h:
                    icon_h = size_h
                # 重新设置logo的尺寸
                icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
                w = int((img_w - icon_w) / 2)
                h = int((img_h - icon_h) / 2)
                img.paste(icon, (w, h), icon)
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                qr_code_img = base64.b64encode(buffer.getvalue())
            record.update({'qr_code': qr_code_img})

    app_id = fields.Many2one('melon.application.manager', u'应用名称', tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string=u'应用详情', attachment=True,help='只能上传一个apk文件')
    qr_code = fields.Image(string='二维码', compute="_generate_qr_code", store=True, attachment=True)
    avatar_1920 = fields.Image("二维码预览", related='qr_code', store=True)
    qr_code_url = fields.Char(u'下载地址', compute="_get_qr_code_url", store=True)
    image_name = fields.Char(u'图片名称')

    # 基础配置
    name = fields.Char(u'策略名称', tracking=True, )
    version_code = fields.Char(u'版本号', tracking=True, )
    app_size = fields.Float(u'应用大小', help='M', compute="_get_qr_code_url", store=True)
    package_name = fields.Char(u'包名', tracking=True)
    upgrade_style = fields.Selection([('recomend', '推荐升级'), ('force', '强制升级')], string=u'升级方式',
                                     default='recomend', tracking=True)
    start_cond = fields.Selection([('now', '立即升级'), ('inverse', '定时升级')], string=u'启动条件', default='now', tracking=True, )
    upgrade_time = fields.Datetime(string='升级时间', tracking=True)
    specify_version_id = fields.Many2one('melon.application.version', u'指定版本', tracking=True)

    # 版本管理
    is_published = fields.Selection([('published', '已发布'), ('unpublished', '未发布')], string=u'发布状态',tracking=True, default='published')
    is_current_version = fields.Selection([('current', '当前版本'), ('history', '历史版本')], string=u'更新状态',tracking=True, default='current')

    # 升级内容
    upgrade_text = fields.Html(u'升级内容',tracking=True)

    @api.constrains('attachment_ids')
    def app_attachment_constrains(self):
        for record in self:
            if record.attachment_ids:
                if (record.attachment_ids[0].name).split('.')[-1]!='apk':
                    raise ValidationError('注意：只能上传apk文件')

    @api.depends('attachment_ids')
    def _get_qr_code_url(self):
        root_url = self.env['ir.config_parameter'].sudo().get_param('apk_file_url')
        for order in self:
            file_url = ''
            page_size = 0.0
            if order.attachment_ids:
                for line in order.attachment_ids[0]:
                    file_url = "%s/ad/content/%s-%s" % (root_url, str(line.id), line.checksum)
                    page_size = line.file_size / 1048576
            order.qr_code_url = file_url
            order.app_size = page_size

    @api.onchange('attachment_ids')
    def get_version_code(self):
        # 检查版本号等信息
        package_name = ''
        app_version = ''
        application_name = ''
        if self.attachment_ids:
            line = self.attachment_ids[0]
            file_store = line.store_fname
            file_path = line._full_path(file_store)
            output = os.popen("aapt d badging %s" % file_path).read()
            if output:
               package_name = re.compile(r"package: name='(\S+)'").findall(output)[0]
               app_version = re.compile(r"versionName='(\S+)'").findall(output)[0]
               application_name = re.compile("application-label:'(.+)'").findall(output)[0]
        self.name = application_name
        self.version_code = app_version
        self.package_name = package_name

    def set_published(self):
        """ 发布"""
        active_ids = self.env.context.get('active_ids')
        version_obj = self.env['melon.application.version']
        publish_dict_ids = version_obj.search([('is_published', '=', 'unpublished'), ('id', 'in', tuple(active_ids))])
        if publish_dict_ids:
            publish_dict_ids.write({'is_published': 'published'})

    def set_current_version(self):
        """ 设定当前版本"""
        active_ids = self.env.context.get('active_ids')
        version_obj = self.env['melon.application.version']
        current_dict_ids = version_obj.search([('is_current_version', '=', 'history'), ('id', 'in', tuple(active_ids))])
        if current_dict_ids:
            current_dict_ids.write({'is_current_version': 'current'})

