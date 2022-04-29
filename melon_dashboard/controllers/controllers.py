# -*- coding: utf-8 -*-

from collections import OrderedDict
from odoo import http, _
from odoo.http import request, route
import os
import jinja2
from odoo.http import request
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/static/templates")
env = Environment(loader=templateLoader)


class SearchController(http.Controller):

    @http.route('/iframe/bim', type='http', auth="public", csrf=False)
    def bim_test_html(self, **post):
        cr, uid, context, pool = request.cr, request.session.uid, request.context, request.env
        template = env.get_template('/bim_h5/zh_CN/index.html')
        values = {}
        demo = {}
        values['users'] = request.env.user
        html = template.render(object=values,tt=demo)
        return html

    @http.route('/iframe/board', type='http', auth="public", csrf=False)
    def bim_html(self, **post):
        template = env.get_template('/board/index.html')
        values = {}
        values['users'] = request.env.user
        html = template.render(object=values)
        return html

    @http.route('/iframe/bigdata', type='http', auth="public", csrf=False)
    def big_data_html(self, **post):
        template = env.get_template('/bigdata/pages/index.html')
        values = {}
        values['users'] = request.env.user
        html = template.render(object=values)
        return html

    @http.route('/iframe/mqtt/iot', type='http', auth="public", csrf=False)
    def mqtt_iot_html(self, **post):
        template = env.get_template('/mqtt/index.html')
        values = {}
        values['users'] = request.env.user
        html = template.render(object=values)
        return html

    @http.route('/iframe/work/bench', type='http', auth="public", csrf=False)
    def work_bench_html(self, **post):
        template = env.get_template('/work_bench/index.html')
        values = {}
        works = [ {
                'title': '测试22222222',
                'time': '2022-02-07'
            }
            , {
                'title': '测试333333333',
                'time': '2022-02-09'
            }
            , {
                'title': '测试39999',
                'time': '2022-02-10'
            }
        ]
        values['works'] = works
        local = [
            {'value': 1048, 'name': 'Search Engine'},
            {'value': 735, 'name': 'Direct'},
            {'value': 580, 'name': 'Email'},
            {'value': 484, 'name': 'Union Ads'},
            {'value': 300, 'name': 'Video Ads'}
        ]
        html = template.render(object=values, local=local)
        return html

    @http.route('/iframe/echarts/demo', type='http', auth="public", csrf=False)
    def echarts_demo_html(self, **post):
        template = env.get_template('/echarts_demo/index.html')
        values = {}
        values['users'] = request.env.user
        html = template.render(object=values)
        return html
