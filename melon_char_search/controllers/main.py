# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, http, fields
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.osv import expression
from odoo.tools import float_round, float_repr
from odoo.service import db, security


class MelonController(http.Controller):

    # @http.route('/about/')
    # def about(self):
    #     return self._render_template('about.html', **{'user': 'username'})

    @http.route('/api/v1/page/0', type='json', auth='none')
    def dtcloud_trash_demo(self, **kwargs):
        """案例：位作分页处理，仅仅返回一个字典，再取里面的data数据"""
        data = request.jsonrequest
        res_data = []
        model = data.get('model')
        search_fields = data.get('fields')
        # domain = data.get('domain')
        query = data.get('query')
        pages = data.get('pages')
        offset = 0
        limit = 10
        order = 'id DESC'
        if pages:
            offset = pages.get('offset')
            limit = pages.get('limit')
            order = pages.get('order')
        search_obj = request.env[model].sudo().search([('name', 'ilike', query)], limit=limit, offset=offset,
                                                      order=order)
        for record in search_obj:
            val = {'id':record.id}
            for i in search_fields:
                val.update({
                    i: record[i]
                })
            res_data.append(val)
        print(res_data)
        return {
            "search": "Administrator",
            "data": res_data,
            "search_count": len(res_data),
            "errmsg": "ok",
            "errcode": 0,
            "message": "查询成功!"
        }
