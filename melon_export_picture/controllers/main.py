# -*- coding: utf-8 -*-
from odoo import http
import requests
import json
from odoo import api, fields, models, _
from odoo.http import request, route
import base64
import logging
import io

# _logger = logging.getLogger(__name__)
#
#
# class DownloadController(http.Controller):

    # @http.route('/download/excel/api', type='http', auth="public", csrf=False, cors='*')
    # def download_excwl_route(self, **kw):
    #     data = kw['data']
    #     print('data',data)
    #     return http.send_file(data, filename='Picture.xls', as_attachment=True)
