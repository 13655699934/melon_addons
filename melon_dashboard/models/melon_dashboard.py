# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
import logging
import datetime, calendar

_logger = logging.getLogger(__name__)


class MelonDashboard(models.Model):
    _name = 'melon.dashboard'

    @api.model
    def get_data(self):
        this_year = datetime.date.today().year
        data = {
            'block1': self.get_data_block1(this_year),
            'block2': self.get_data_block2(this_year),
            'block3': self.get_data_block3(this_year)
        }
        return data

    @api.model
    def get_data_block1(self, year):
        today = datetime.date.today()
        this_year = today.year
        this_month = today.month
        # sale_obj = self.env['sale.order']
        block1 = {'order_num': [100, 80, 50, 30, 0, 23, 56, 45, 89, 14, 45, 89]}
        # for month in range(1, 13):
        #     if not year:
        #         year = today.year
        #     date_start = '%s-%02d-01' % (year, month)
        #     wday, monthRange = calendar.monthrange(year, month)
        #     date_end = '%s-%02d-%s' % (year, month, monthRange)
        #     domian = [('date_order', '>=', date_start), ('date_order', '<', date_end), ]
        #     block1['order_num'].append(sale_obj.search_count(domian))
        return block1

    @api.model
    def get_data_block2(self, year):
        today = datetime.date.today()
        this_year = today.year
        this_month = today.month
        # sale_obj = self.env['sale.order']
        block2 = {'total': [100, 80, 50, 30, 0, 23, 56, 45, 89, 14, 45, 89],
                  'pay': [25, 36, 56, 98, 15, 0, 0, 30, 0, 0, 86, 14]}
        # for month in range(1, 13):
        #     if not year:
        #         year = today.year
        #     date_start = '%s-%02d-01' % (year, month)
        #     wday, monthRange = calendar.monthrange(year, month)
        #     date_end = '%s-%02d-%s' % (year, month, monthRange)
        #     self._cr.execute("""select sum(total),sum(pay) from
        #                           (select sum(t1.price_total) as total,sum(t1.price_unit*t1.product_uom_qty) as pay
        #                           from sale_order_line t1
        #                           LEFT JOIN sale_order t2 on t1.order_id=t2.id
        #                           where t1.state='sale' and (t2.date_order>'%s' and t2.date_order<'%s')
        #                           GROUP BY t1.id) as tt;""" % (date_start, date_end))
        #     res = self._cr.fetchall()
        #     block2['total'].append(res[0][0] or 0.0)
        #     block2['pay'].append(res[0][1] or 0.0)
        return block2

    @api.model
    def get_data_block3(self, year):
        # sale_obj = self.env['sale.order']
        date_start = '%s-01-01' % year
        date_end = '%s-12-01' % year
        domian = [('date_order', '>=', date_start), ('date_order', '<', date_end)]
        # block3 = {'type_num': {
        #     'A': sale_obj.search_count(domian + [('state', '=', 'draft')]),
        #     'B': sale_obj.search_count(domian + [('state', '=', 'sent')]),
        #     'C': sale_obj.search_count(domian + [('state', '=', 'sale')]),
        # }}
        block3 = {'type_num': {
            'A': 50,
            'B': 90,
            'C': 78,
        }}
        return block3
