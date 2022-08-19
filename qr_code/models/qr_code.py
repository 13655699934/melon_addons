# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from odoo import models, fields, api
import qrcode


class QRCode(models.Model):
    _name = 'melon.qr.code'
    _description = '二维码生成器'

    @api.depends('qr_code_content')
    def _generate_qr_code(self):
        """根据内容生成二维码"""
        for record in self:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
            qr_code_img = False
            qr_code_img_name = False
            if record.qr_code_content:
                qr_code_img_name = record.name + '.png'
                qr.add_data(record.qr_code_content)
                qr.make(fit=True)
                img = qr.make_image()
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                qr_code_img = base64.b64encode(buffer.getvalue())
            record.update({'qr_code': qr_code_img, 'qr_code_name': qr_code_img_name})

    name = fields.Char(u'编号', default=lambda self: self.env['ir.sequence'].next_by_code('melon.qr.code'))
    qr_code_name = fields.Char(string=u'二维码名称', default="qr_code.png")
    qr_code_content = fields.Text(u'二维码内容')
    qr_code = fields.Image(string='二维码', compute="_generate_qr_code", store=True)
    image_512 = fields.Image("Image 512", related="qr_code", max_width=512, max_height=512, store=True)
    image_128 = fields.Image("Image 128", related="qr_code", max_width=128, max_height=128, store=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('melon.qr.code') or 'New'
        return super(QRCode, self).create(vals)
