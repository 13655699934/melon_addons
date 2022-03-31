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


class LargeScreenController(http.Controller):


    @http.route('/iframe/bigdata', type='http', auth="public", csrf=False)
    def big_data_html(self, **post):
        template = env.get_template('/bigdata/pages/index.html')
        values = {}
        values['users'] = request.env.user
        html = template.render(object=values)
        return html


    @http.route('/iframe/smart/logistics', type='http', auth="public", csrf=False)
    def echarts_demo_html(self, **post):
        template = env.get_template('/smart_logistics/index.html')
        values = {}
        values['users'] = request.env.user
        html = template.render(object=values)
        return html

    @http.route('/iframe/smart/community', type='http', auth="public", csrf=False)
    def community_html(self, **post):
        template = env.get_template('/smart_community/index.html')
        values = {}
        values['users'] = request.env.user
        html = template.render(object=values)
        return html

