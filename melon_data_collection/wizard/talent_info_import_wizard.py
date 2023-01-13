# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import xlrd, base64, datetime
from xlrd import open_workbook, xldate_as_tuple
import logging

_logger = logging.getLogger(__name__)


def check_id_data(n):
    """
    校验身份证是否正确
    """
    if len(str(n)) != 18:
        # print("身份证号为[%s],核验失败" % n)
        return 0
    var = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    var_id = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']
    n = str(n)
    sum = 0
    if int(n[16]) % 2 == 0:
        gender = "女"
        same = int(int(n[16]) / 2)
    else:
        gender = "男"
        same = int((int(n[16]) + 1) / 2)
    for i in range(0, 17):
        sum += int(n[i]) * var[i]
    sum %= 11
    if (var_id[sum]) != str(n[17]):
        # print("身份证号为[%s],核验失败" % n)
        return 0
    else:
        return 1



def get_cell_value(sCell, ctype):
    '''
    获取Excel日期格式单元格数据，Python读Excel，返回的单元格内容的类型有5种：
    ctype：
    0 :empty
    1: string
    2: number;
    3: date;
    4:boolean,;
    5:error
    :param sCell: 单元格数据
    :param ctype: 数据类型
    :return:
    '''
    # 44197.0 为2021-01-01对应的excel格式的float值，做辅助用
    y_date = 44197.0
    istime = 0
    # 日期格式
    if sCell == '':
        return False
    sCell = int(sCell)
    if ctype == 3:
        if sCell < 1:
            istime = 1
            sCell = y_date + sCell
        dtime = datetime.datetime(*xldate_as_tuple(sCell, 0))
        strTime = dtime.strftime('%Y-%m-%d')
        # 只包含时间，没有日期 比如：01:31:52
        if istime == 1:
            return strTime[11:]
        else:
            return strTime
    else:
        return sCell



class TalentInfoWizard(models.TransientModel):
    _name = 'import.talent.info.wizard'
    _description = '采集信息'

    data = fields.Binary(u'请选择文件')
    data_filename = fields.Char('附件名')

    def btn_confirm(self):
        """
          有模板可以下载，按照模板整理数据导入
          用xlrd 解析excel中单数据，导入系统模块中
          注意点：1、字段是many2many的，
                   excel里面的数据是用逗号隔开的；
                 2、分别获取excel数据，保存在字典里
                    base_infos 是基础数据部分；
                    projects 是项目信息部分；
        """
        if self.data_filename:
            import_type = self.data_filename.split(".")[-1]
            if import_type != "xls":
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': u'文件格式错误！',
                        'message': '请上传格式为"xls"格式的Excel文件！',
                        'sticky': False,
                        'type': 'warning',
                    },
                }
        for_obj = self.env['talent.base.inform'].sudo()
        res_id = self.env.context.get('res_id')
        excel_obj = xlrd.open_workbook(file_contents=base64.decodebytes(self.data))
        sheets = excel_obj.sheets()
        base_infos = self.get_base_info_data(sheets[0])
        if isinstance(base_infos, str):
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': u'数据校验',
                    'message': base_infos,
                    'sticky': True,
                    'type': 'warning',
                    'next': {
                        'type': 'ir.actions.act_window_close'
                    },
                },
            }
        projects = ""
        if len(sheets) > 1:
            projects = self.get_project_data(sheets[1])
            if not base_infos:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': u'数据校验',
                        'message': '请先在excel里填写数据！',
                        'sticky': False,
                        'type': 'warning'
                    },
                }
        for item in base_infos:
            # 创建信息主表
            main_id = for_obj.create(item)
            if projects:
                eff_values = list(filter(lambda x: x['id_number'] == item['ID_number'], projects))
                pro_list = []
                for line in eff_values:
                    pro_list.append(
                        (0, 0, {'name': line['name'], 'code': line['code'], 'description': line['description']}))
                main_id.write({'project_info_ids': pro_list})
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': u'数据校验',
                'message': '数据导入成功',
                'sticky': True,
                'type': 'success',
                'next': {
                    'type': 'ir.actions.act_window_close'
                },
            },
        }
        return notification

    def get_base_info_data(self, sh):
        """获取基本信息"""
        err_msg, professional_err_msg = [], []
        res_id = self.env.context.get('res_id')
        values_line = []
        for row in range(1, sh.nrows):
            if len(list(filter(lambda _: _, sh.row_values(row)))) < 3:  # 排除同一sheet中的下拉列表的数据
                continue
            name = sh.cell(row, 0).value
            age = sh.cell(row, 1).value
            ID_number = sh.cell(row, 2).value
            if  ID_number:
                result = check_id_data(ID_number)
                if result == 0:
                    err_msg.append(ID_number)
                for_obj = self.env['talent.base.inform'].sudo()
                old_records = for_obj.search([('ID_number', '=', ID_number), ('by_import', '=', True)])
                old_records.sudo().unlink()
            graduation_school = sh.cell(row, 3).value
            major_studied = sh.cell(row, 4).value
            values_line.append({
                'name': name,
                'age': age,
                'ID_number': ID_number,
                'graduation_school': graduation_school,
                'major_studied': major_studied,
                'by_import': True
            })

        if err_msg and not professional_err_msg:
            message = '数据校验失败,下列身份证号无效【%s】' % ','.join(err_msg)
            return message
        elif not err_msg and professional_err_msg:
            message = ''.join(professional_err_msg)
            return message
        elif err_msg and professional_err_msg:
            message = '数据校验失败,下列身份证号无效【%s】。并且' % ','.join(err_msg) + ''.join(professional_err_msg)
            return message
        return values_line

    def get_project_data(self, sh):
        """获取项目表信息"""
        result = []
        for row in range(1, sh.nrows):
            item = {
                'id_number': sh.cell(row, 0).value or '',
                'code': sh.cell(row, 1).value or '',
                'name': sh.cell(row, 2).value or '',
                'description': sh.cell(row, 3).value or '',
            }
            result.append(item)
        return result
