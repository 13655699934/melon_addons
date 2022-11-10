# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import models, fields, tools, _


class AttachZipDemo(models.Model):
    _name = "attach.zip.download.demo"
    _description = "测试表单"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'名称')
    # 附件: field1 = fields.Many2many("B","a_b_rel","a","b",string="字段1")
    attachment_ids = fields.Many2many('ir.attachment', 'a_attach_zip_demo_rel', 'azp_id', 'att_id', string=u'附件',
                                      index=True)
    test_data = fields.Binary('测试附件', attachment=True)
    test_filename = fields.Char('测试附件名')
    demo_data = fields.Binary('Data', attachment=True)
    demo_filename = fields.Char('Data name')

    @api.model
    def create(self, vals):
        result = super(AttachZipDemo, self).create(vals)
        result.set_binary_name(vals)
        return result

    def write(self, vals):
        result = super(AttachZipDemo, self).write(vals)
        self.set_binary_name(vals)
        # self.env['watermark.design.order'].set_value([1])
        return result

    def set_binary_name(self, vals):
        """
            binary_fields里面是表单存的 binary字段，需要按下面格式处理
        """
        binary_fields = {'test_data': 'test_filename', 'demo_data': 'demo_filename'}
        for k, v in binary_fields.items():
            if k not in vals:
                continue
            attr_id = self.env['ir.attachment'].sudo().search(
                [('res_id', '=', self.id), ('res_model', '=', self._name), ('res_field', '=', k)], limit=1)
            if attr_id:
                attr_id.write({'name': self[v]})

    def action_download_attachment(self):
        """获取表单相关的模型打包下载
           注意：1、Binary类型字段设置【 attachment=True】;
                2、Binary类型字段存在附件表里面的name需要改写，原生存储的为字段的名字;
                3、ir.attachment表指定第三方表时，附件表里不存res_id 需要与'a_attach_zip_demo_rel'中间表获取;
        """
        att_ids = []
        for order in self:
            self._cr.execute(
                """SELECT id FROM ir_attachment WHERE  res_model='%s' and res_id=%d""" % (
                    self._name, order.id))
            attach_ids = [row[0] for row in self._cr.fetchall()]
            self._cr.execute("""SELECT att_id FROM a_attach_zip_demo_rel WHERE azp_id=%d""" % order.id)
            attach_zip_ids = [row[0] for row in self._cr.fetchall()]
            if attach_ids:
                att_ids.extend(attach_ids)
            if attach_zip_ids:
                att_ids.extend(attach_zip_ids)
        if not att_ids:
            raise ValidationError(u'当前单据无附件,无法下载！')
        url = '/web/attachment/download_document?att_ids=%s' % att_ids
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    # def btn_test(self):
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'type': 'warning',
    #             'message': 'i am client',
    #             'next': {
    #                 'type': 'ir.actions.act_window',
    #                 'name': 'Next',
    #                 'res_model': 'res.users',
    #                 'view_type': 'list',
    #                 'target': 'new',
    #                 'views': [[False, 'list']]
    #             },
    #         }
    #     }
