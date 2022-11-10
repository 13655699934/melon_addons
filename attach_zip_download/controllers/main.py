# -*- coding: utf-8 -*-
import base64
import logging
import base64
import xlwt
from io import BytesIO
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
import zipfile
from datetime import datetime
from odoo import http, exceptions
from odoo.http import request
from odoo.http import content_disposition
import ast
_logger = logging.getLogger(__name__)
import time
# 获取时间戳
def t_stamp():
    t = time.time()
    t_stamp = int(t)
    print('当前时间戳:', t_stamp)
    return t_stamp



class Binary(http.Controller):


    @http.route('/web/attachment/download_document', type='http', auth="public")
    def download_document(self, att_ids, **kw):
        new_tab = ast.literal_eval(att_ids)
        attachment_ids = request.env['ir.attachment'].sudo().search([('id', 'in', tuple(new_tab))])
        file_dict = {}
        for attachment_id in attachment_ids:
            file_store = attachment_id.store_fname
            if file_store:
                file_name = attachment_id.name
                file_path = attachment_id._full_path(file_store)
                file_dict["%s:%s" % (file_store, file_name)] = dict(path=file_path, name=file_name)
        print ('---------file_dict',file_dict)
        zip_filename = datetime.now()
        zip_filename = "%s.zip" % zip_filename
        bitIO = BytesIO()
        zip_file = zipfile.ZipFile(bitIO, "w", zipfile.ZIP_DEFLATED)
        for file_info in file_dict.values():
            zip_file.write(file_info["path"], file_info["name"])
        print ('zip_file----',zip_file)
        zip_file.close()
        return request.make_response(bitIO.getvalue(),
                                     headers=[('Content-Type', 'application/x-zip-compressed'),
                                              ('Content-Disposition', content_disposition(zip_filename))])


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
            worksheet.write(row, 0, line.name if line.name else '')
            worksheet.write(row, 1, line.sex if line.sex else '')
            worksheet.write(row, 2, line.age if line.age else '')
            row = row + 1
            # 保存
        buffer = BytesIO()
        workbook.save(buffer)
        return base64.encodebytes(buffer.getvalue())


    @http.route('/web/excel/download', type='http', auth="public",csrf=False)
    def download_excel(self, task_ids, **kw):
        file_dict = {}
        task_ids = ast.literal_eval(task_ids)
        task_ids=request.env['demo.user'].browse(task_ids)
        stream = BytesIO()
        try:
            with zipfile.ZipFile(stream, 'w') as doc_zip:
                i=1
                for task in task_ids:
                   doc_zip.writestr('test_%s.xls'%str(i), base64.b64decode(self.generate_excel(task)),
                                     compress_type=zipfile.ZIP_DEFLATED)
                   i+=1
        except zipfile.BadZipfile:
            _logger.exception("BadZipfile exception")
        content = stream.getvalue()
        headers = [
            ('Content-Type', 'zip'),
            ('X-Content-Type-Options', 'nosniff'),
            ('Content-Length', len(content)),
            ('Content-Disposition', content_disposition('Demo—20220608.zip'))
        ]
        return request.make_response(content, headers)
