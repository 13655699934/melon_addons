# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import odoo
from odoo import http, _
from odoo.osv import expression
from jinja2 import Environment, FileSystemLoader
import logging
from odoo import api, fields, models
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)
from odoo.http import request
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/static/templates/")
env = Environment(loader=templateLoader)


def get_date_range(begin, end, select):
    """
      year获取：两者之间的年份：[{'2021': 0}, {'2022': 0}]
      month获取：[{'2021-01': 0}, {'2021-02': 0}, {'2021-03': 0}]
    """
    from datetime import datetime, timedelta
    if select == 'year':
        begin_date = datetime.strptime(begin, "%Y")
        end_date = datetime.strptime(end, "%Y")
    else:
        begin_date = datetime.strptime(begin, "%Y-%m")
        end_date = datetime.strptime(end, "%Y-%m")
    begin_year, end_year = begin_date.year, end_date.year
    begin_month, end_month = begin_date.month, end_date.month
    data_dict = {}
    if select == 'month':
        if begin_year == end_year:
            for i in range(begin_month, end_month + 1):
                data_dict.update({'%s-%s' % (begin_year, '0%s' % i if i < 10 else i): 0})
        else:
            for year in range(begin_year, end_year + 1):
                if begin_year == year and begin_month:
                    for i in range(begin_month, 13):
                        data_dict.update({'%s-%s' % (year, '0%s' % i if i < 10 else i): 0})
                elif begin_year < year < end_year:
                    for i in range(1, 13):
                        data_dict.update({'%s-%s' % (year, '0%s' % i if i < 10 else i): 0})
                else:
                    for i in range(1, end_month + 1):
                        data_dict.update({'%s-%s' % (end_year, '0%s' % i if i < 10 else i): 0})
    else:
        for i in range(begin_year, end_year + 1):
            data_dict.update({'%s' % i: 0})
    return data_dict


class AnalysisReportApi(http.Controller):

    @http.route('/data_analysis_report', type='http', auth="public")
    def data_analysis_report_api(self, **kw):
        """

        :param kw:
        :return:
        """
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        user = pool['res.users'].sudo().browse(request.session.uid)
        values = {'company': user.company_id}
        api_url=request.httprequest.url_root
        try:
            template = env.get_template('melon/zh_CN/index.html')
            html = template.render(object=values)
        except IOError:
            template = env.get_template('zh_CN/404.html')
            html = template.render(object=values,api_url=api_url)
        return html

    @http.route('/crm/sale/api', type='http', auth="public", csrf=False, cors='*')
    def get_crm_partner_statistics(self, **kw):
        """
          草稿   try_data
          询价   consul_data
          确认 conversion_data
          取消 occupancy_data
        """
        box1_data = {
            "try_data": {
                "total": 10,
                "count": 24
            },
            "consul_data": {
                "total": 60,
                "count": 13
            },
            "conversion_data": {
                "total": 30,
                "count": 76,
            },
            "occupancy_data": {
                "total": 70,
                "count": 34,
            }
        }
        return json.dumps({"success": True, "message": "success", "code": 200, "data": box1_data})

    @http.route('/crm/map/data/api', type='http', auth="public", csrf=False, cors='*')
    def get_crm_map_data_api(self, **kw):
        """
        {
        }
        """
        partner_obj = request.env['res.partner'].sudo()
        box9_data = {}
        customer = []
        all_elders = partner_obj.search([])
        for order in all_elders:
            customer.append({
                'name': order.name or '',
                'age': 30,
                'coords': [120.65177234752295,31.427854797500984],
                'room_type': '',
                'nursing_type': ''
            })
        melon = {
            'name': '测试',
            'coords': [120.65177234752295,31.427854797500984],
        }
        box9_data = {'customer': customer, 'institution': melon}
        return json.dumps({"success": True, "message": "success", "code": 200, "data": box9_data})

    @http.route('/crm/bar/category/api', type='http', auth="public", csrf=False, cors='*')
    def get_crm_bar_category_api(self, **kw):
        """
           客户职业:customer_occ_data
        """
        box5_data = {
                     'customer_occ_data': {"x_data": ['IT','项目经理','实施','运维','产品'], 'y_data': [23,3,4,55,67]}}

        return json.dumps({"success": True, "message": "success", "code": 200, "data": box5_data})


    @http.route('/crm/customer/order/api', type='http', auth="public", csrf=False, cors='*')
    def get_crm_customer_data_api(self, **kw):
        """
        客户数据
          limit:
          page:
          username:
        """
        # data = request.httprequest.data
        # kw_data = json.loads(data)
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        kw_data = kw
        order_obj = request.env['res.partner'].sudo()
        partners = []
        # counts = order_obj.search_count([])
        if kw_data.get('username'):
            counts = order_obj.search_count([('name','ilike',kw_data.get('username'))])
            alone_elder = order_obj.search([('name','ilike',kw_data.get('username'))])
            if alone_elder:
                for line in alone_elder:
                    partners.append({
                        'username': line.name or '',
                        'phone_number': '13655699934',
                        'age': 29,
                        'state': '未入住',
                    })
        else:
            offset = 5 * (int(kw_data['page']) - 1)
            counts = order_obj.search_count([],)
            all_order = order_obj.search([], limit=5, offset=offset)
            for line in all_order:
                partners.append({
                    'username': line.name or '',
                    'phone_number': '13655699934',
                    'age': 31,
                    'state': 'ok',
                })
        return json.dumps({"success": True, "message": "success", "code": 200, "data": partners, 'count': counts})