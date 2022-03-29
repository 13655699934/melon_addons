from odoo import _, api, fields, models
import base64
import io
import xlsxwriter
from PIL import Image
from io import BytesIO
from odoo import fields, models


class ExportImageExcelWizard(models.TransientModel):
    _name = "export.image.excel.wizard"
    _description = "Export Image Excel wizard"

    def get_model_domain(self):
        field_ids = self.env["ir.model.fields"].search([("ttype", "=", "binary")])
        model_ids = (
            field_ids.mapped("model_id")
                .sorted("name")
                .filtered(lambda m: not m.model.startswith("ir.") and not m.transient)
        )
        return [("id", "in", model_ids.ids)]

    model_id = fields.Many2one("ir.model", string="Model", domain=get_model_domain)
    binary_field_id = fields.Many2one("ir.model.fields", string="Image Fields")
    file_data = fields.Binary(u'Export File')

    def btn_confirm(self):
        """导出excel入口函数"""
        model_name = self.model_id.model
        image_name = self.binary_field_id.name
        match_obj = self.env[model_name].sudo()
        records = match_obj.search([])
        output = io.BytesIO()
        book = xlsxwriter.Workbook(output)
        sheet = book.add_worksheet('Picture')
        num1 = 1
        count = 1
        for record in records:
            if record[image_name]:
                buf_image = io.BytesIO(base64.b64decode(record[image_name]))
                sheet.write('A%s' % (num1), record.name)
                sheet.insert_image('D%s' % (num1), "00%s.jpg" % (count),
                                   {'image_data': buf_image, 'x_scale': 0.5, 'y_scale': 0.5, 'positioning': 5})
                num1 += 5
                num1 += 1
        book.close()
        wiz_id = self.env['export.image.excel.wizard'].create({'file_data': base64.encodebytes(output.getvalue())})
        value = dict(
            type='ir.actions.act_url',
            target='self',
            url='/web/content?model=%s&id=%s&field=file_data&download=true&filename=Picture.xlsx' % (
                self._name, wiz_id.id),
        )
        return value
