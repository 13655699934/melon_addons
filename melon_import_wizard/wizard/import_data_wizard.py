# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import xlrd, base64, datetime
from xlrd import xldate_as_tuple


class ImportWizard(models.TransientModel):
    _name = 'import.data.wizard'
    _description = u'导入数据模板'

    data = fields.Binary(u'导入Excel文件')

    def btn_confirm(self):
        field_order = ['name', 'code', 'order_name', 'ded_expenses', 'close_amount','notes']
        import_model = self.env['melon.data.order']
        # 跟python版本有关：decodestring或者decodebytes
        # excel_obj = xlrd.open_workbook(file_contents=base64.decodestring(self.data))
        excel_obj = xlrd.open_workbook(file_contents=base64.decodebytes(self.data))
        # sheets=excel_obj.sheets()  读取所有sheet表
        sh = excel_obj.sheets()[0]  # 读取第一个sheet表
        # todo 日期格式是否需要校验提示？
        for row in range(1, sh.nrows):  # 循环所有行，从第二行读起
            record = {}
            i = 0
            for f in field_order:
                record.update({f: sh.cell(row, i).value})
                i += 1
            import_model.sudo().create(record)
        # 导入数据后，刷新当前页面
        return {'type': 'ir.actions.client', 'tag': 'reload', }
