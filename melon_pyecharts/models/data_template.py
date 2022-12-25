# -*- coding: utf-8 -*-
'''
odoo
'''
from odoo import api, fields, models, tools, _
import time
from pyecharts.charts import Bar
import os
import logging
from odoo.exceptions import ValidationError

from pyecharts import options as opts
from pyecharts.charts import Pie

_logger = logging.getLogger(__name__)


class DataTemplate(models.Model):
    _name = 'data.template'
    _description = u'数据模板'

    name = fields.Char('名称')
    line_ids = fields.One2many('data.template.line', 'temp_id', string='测试数据')

    pie_charts = fields.Text('饼状图')
    bar_charts = fields.Text('柱状图')

    @api.model
    def create(self, vals):
        res = super(DataTemplate, self).create(vals)
        if res.line_ids:
            res.sudo().action_generate_charts()
        return res

    def action_generate_charts(self):
        """"""
        key = []
        value = []
        for obj in self.line_ids:
            key.append(obj.key)
            value.append(obj.value)
        echarts_path = self.env['ir.config_parameter'].sudo().get_param('echarts_save_path', default='')
        if echarts_path=='0':
            raise ValidationError('请先设置echarts图表存储路径,例：/opt/echarts_dir')
        c_pt = "%s/pie_set_color_%d.html" % (echarts_path,self.id)
        print('c_pt', c_pt)
        print('key', key)
        print('value', value)
        c = (
            Pie()
                .add("", [list(z) for z in zip(key, value)])
                .set_colors(["blue", "green", "yellow", "red", "pink"])
                .set_global_opts(title_opts=opts.TitleOpts(title="Pie-%s" % self.name))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                .render(c_pt)
        )
        self.pie_charts = open(c_pt, 'rb').read()
        os.remove(c_pt)

        b_pt = "%s/bar_with_brush_%d.html" % (echarts_path,self.id)
        bar = (
            Bar()
                .add_xaxis(key)
                .add_yaxis(self.name, value)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="Bar-%s" % self.name, subtitle=self.name or ''),
                brush_opts=opts.BrushOpts(),
            )
                .render(b_pt)
        )
        print('b_pt',b_pt)
        print('b_pt',b_pt)
        self.bar_charts = open(b_pt, 'rb').read()
        os.remove(b_pt)


    def write(self, vals):
        return super(DataTemplate, self).write(vals)


class DataTemplateLine(models.Model):
    _name = 'data.template.line'
    _description = u'数据模板'

    temp_id = fields.Many2one('data.template', '模板')
    name = fields.Char('名称')
    key = fields.Char('键')
    value = fields.Float('值')
