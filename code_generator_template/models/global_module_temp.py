# -*- coding: utf-8 -*-
from odoo import models, fields, api
import base64
import csv
import io
import os
import lxml.etree as ET
import base64
import black

FIELD_TYPES = [(key, key) for key in sorted(fields.Field.by_type)]


class GlobalModuleTemp(models.Model):
    _name = "global.module.temp"
    _description = "模型创建模版"

    name = fields.Char('模型逻辑名', required=True)
    class_name = fields.Char('模型类名', required=True)
    description = fields.Char('模型描述', required=True)
    field_line_ids = fields.One2many('global.temp.field.line', 'order_id', string='字段列表')
    # py文件
    xml_binary = fields.Binary('XML代码文件', help="生成的XML代码文件", readonly=True)
    xml_binary_name = fields.Char('File Name')

    # xml文件
    py_binary = fields.Binary('Python代码文件', help="生成的Python代码文件", readonly=True)
    py_binary_name = fields.Char('File Name')

    # csv文件
    csv_binary = fields.Binary('csv代码文件', help="生成的csv代码文件", readonly=True)
    csv_binary_name = fields.Char('File Name')

    # 生成代码log
    py_logs = fields.Text('Python代码')
    xml_logs = fields.Text('XML代码')
    csv_logs = fields.Text('CSV代码')

    def action_auto_all(self):
        """调用三个函数"""
        self.action_auto_py()
        self.action_auto_xml()
        self.action_auto_csv()

    def action_auto_py(self):
        self.py_binary = False
        self.py_binary_name = False

        name_str = str(self.name).replace('.', '_')

        # **生成 Python 代码**
        all_data = f"""# -*- coding: utf-8 -*-
from odoo import models, fields

class {self.class_name}(models.Model):
    _name = '{self.name}'
    _description = '{self.description}'
"""

        field_template = {
            "many2one": "    {name} = fields.Many2one('{model}', string='{desc}', readonly={readonly}, required={required})",
            "many2many": "    {name} = fields.Many2many('{model}', '{relation}', '{col1}', '{col2}', string='{desc}', readonly={readonly}, required={required})",
            "one2many": "    {name} = fields.One2many('{model}', '{related_field}', string='{desc}', readonly={readonly}, required={required})",
            "char": "    {name} = fields.Char(string='{desc}', readonly={readonly}, required={required})",
            "integer": "    {name} = fields.Integer(string='{desc}', readonly={readonly}, required={required})",
            "float": "    {name} = fields.Float(string='{desc}', readonly={readonly}, required={required})",
            "boolean": "    {name} = fields.Boolean(string='{desc}', readonly={readonly}, required={required})",
            "selection": "    {name} = fields.Selection(selection={selection}, string='{desc}', readonly={readonly}, required={required})",
            "date": "    {name} = fields.Date(string='{desc}', readonly={readonly}, required={required})",
            "datetime": "    {name} = fields.Datetime(string='{desc}', readonly={readonly}, required={required})",
            "text": "    {name} = fields.Text(string='{desc}', readonly={readonly}, required={required})",
            "binary": "    {name} = fields.Binary(string='{desc}', readonly={readonly}, required={required})",
            "html": "    {name} = fields.Html(string='{desc}', readonly={readonly}, required={required})"
        }

        for line in self.field_line_ids:
            params = {
                "name": line.name,
                "desc": line.field_description,
                "readonly": line.readonly,
                "required": line.required
            }

            if line.type in field_template:
                if line.type == "selection":
                    params["selection"] = [(i.name, i.value) for i in line.selection_ids]
                elif line.type in ["many2one", "one2many"]:
                    params["model"] = line.model_id.model
                elif line.type == "many2many":
                    params.update({
                        "model": line.model_id.model,
                        "relation": line.relation_table,
                        "col1": line.column1,
                        "col2": line.column2
                    })
                elif line.type == "one2many":
                    params["related_field"] = line.related_field

                all_data += field_template[line.type].format(**params) + "\n"

        # **存储到 Odoo**
        self.py_logs = all_data
        self.py_binary_name = f"{name_str}.py"
        self.py_binary = base64.b64encode(all_data.encode('utf-8')).decode('utf-8')

    def action_auto_xml(self):
        self.xml_binary = False
        self.xml_binary_name = False

        name_str = str(self.name).replace('.', '_')

        head_data = """<?xml version="1.0" encoding="utf-8"?>
        <odoo>
        """
        fields_data = "".join([f'\n                <field name="{line.name}"/>' for line in self.field_line_ids])

        list_data = f"""
        <record id="{name_str}_list_view" model="ir.ui.view">
            <field name="name">{self.name}.list</field>
            <field name="model">{self.name}</field>
            <field name="arch" type="xml">
                <list string="{self.description}">{fields_data}
                </list>
            </field>
        </record>"""

        form_data = f"""
        <record id="{name_str}_form_view" model="ir.ui.view">
            <field name="name">{self.name}.form</field>
            <field name="model">{self.name}</field>
            <field name="arch" type="xml">
                <form string="{self.description}">
                    <sheet>
                        <group>{fields_data}
                        </group>
                    </sheet>
                </form>
            </field>
        </record>"""

        action_data = f"""
        <record id="action_{name_str}_view" model="ir.actions.act_window">
            <field name="name">{self.description}</field>
            <field name="res_model">{self.name}</field>
            <field name="view_mode">list,form</field>
        </record>"""

        menu_data = f"""
        <menuitem id="menu_{name_str}_root"
            name="{self.description}"
            sequence="1"
            action="action_{name_str}_view"/>"""

        foot_data = "</odoo>"

        all_data = head_data + list_data + form_data + action_data + menu_data + foot_data

        # **存储到 Odoo**
        self.xml_logs = all_data
        self.xml_binary_name = f"{name_str}_views.xml"
        self.xml_binary = base64.b64encode(all_data.encode('utf-8')).decode('utf-8')

    def action_auto_csv(self):
        self.csv_binary = False
        self.csv_binary_name = False
        name_str = self.name.replace('.', '_')

        # **构造 CSV 数据**
        csv_data = [
            ["id", "name", "model_id:id", "group_id:id", "perm_read", "perm_write", "perm_create", "perm_unlink"],
            [f"access_{name_str}", name_str, f"model_{name_str}", "base.group_user", 1, 1, 1, 1]
        ]

        # **格式化 CSV**
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(csv_data)
        all_data = csv_buffer.getvalue()

        # **存储到 Odoo**
        self.csv_logs = all_data
        self.csv_binary_name = "ir.model.access.csv"
        self.csv_binary = base64.b64encode(all_data.encode('utf-8')).decode('utf-8')


class GlobalTempFieldLine(models.Model):
    _name = "global.temp.field.line"
    _description = "字段列表"

    order_id = fields.Many2one('global.module.temp', string='模型创建模版')
    name = fields.Char('字段名称')
    field_description = fields.Char('字段描述')
    model_id = fields.Many2one('ir.model', string='关联模型')
    related_field = fields.Char(string='关联字段')
    help = fields.Text(string='字段帮助', translate=True)
    type = fields.Selection(selection=FIELD_TYPES, string='字段类型', required=True)
    relation_table = fields.Char('关系表')
    column1 = fields.Char(string='列1')
    column2 = fields.Char(string="列2")
    required = fields.Boolean('必填')
    readonly = fields.Boolean('只读')
    selection_ids = fields.One2many("temp.fields.selection", "field_id", string="选项")


class TempFieldSelection(models.Model):
    _name = "temp.fields.selection"
    _description = "Selection选项"

    field_id = fields.Many2one("global.temp.field.line", string='模型创建模版')
    name = fields.Char('逻辑值')
    value = fields.Char('显示值')
