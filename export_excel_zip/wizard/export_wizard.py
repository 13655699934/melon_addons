from odoo import models, fields, api
import base64
import xlwt
from io import BytesIO
import logging
_logger = logging.getLogger(__name__)


class UserExport(models.TransientModel):
    _name = "user.export"
    _description = "导出成excel"

    file = fields.Binary('文件')

    def generate_excel(self, task_ids):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('任务清单')
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = '宋体'  # 字体
        font.bold = True  # 加粗
        font.height = 20 * 10  # 字体大小
        style.font = font  # 为样式设置字体

        # 添加列的标题
        header = ['姓名', '性别', '年龄']
        for col in range(len(header)):
            worksheet.write(0, col, header[col], style)
        row = 1
        for line in task_ids:
            print (line.name)
            print (line.sex)
            print (line.age)
            worksheet.write(row, 0, line.name if line.name else '')
            worksheet.write(row, 1, line.sex if line.sex else '')
            worksheet.write(row, 2, line.age if line.age else '')
            row = row + 1
            # 保存
        buffer = BytesIO()
        workbook.save(buffer)
        return base64.encodebytes(buffer.getvalue())

    def action_export_data(self):
        # 获取id
        context = dict(self._context or {})
        task_ids = context.get('active_ids')
        # 查出数据
        url = '/web/excel/download?task_ids=%s' % task_ids
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }


    # def action_export_data(self):
    #     # 获取id
    #     context = dict(self._context or {})
    #     task_ids = context.get('active_ids')
    #     # 查出数据
    #     task_ids = self.env['demo.user'].browse(task_ids)
    #     # 调用自定义excel模板
    #     res = self.create({'file': self.generate_excel(task_ids)})
    #     file_name = 'DEMO_USER'
    #     excel_url = '/web/content?model=%s&id=%s&field=file&download=true&filename=%s.xls' % (self._name, res.id, file_name)
    #     value = dict(
    #         type = 'ir.actions.act_url',
    #         target = 'self',
    #         url = excel_url,
    #     )
    #     return value
