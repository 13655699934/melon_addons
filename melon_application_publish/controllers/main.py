# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime, timedelta
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

ModuleBasedir = os.path.dirname(os.path.dirname(__file__))


class AppPublishApi(http.Controller):

    @http.route('/api/version/upgrade', type="json", auth="none", csrf=False, cors='*', ext=True)
    def sync_apk_version_api(self, **kw):
        """
           同步apk版本
           逻辑是：找到此应用，大于当前版本的 当前已发布的版本
           {
                "jsonrpc":"2.0",
                "method":"call",
                "params":{
                    "version":"2.3.9",
                    "appid":"34789499",
                    "appkey":"1233erfy9999"
                }
           }
        """
        re_data = {
            "jsonrpc": "2.0",
            "id": 1
        }
        version_obj = request.env['melon.application.version'].sudo()
        data = request.jsonrequest
        appid = data['params']["appid"]
        params_version = data['params']["version"]
        appkey = data['params']["appkey"]
        domain = [('app_id.appid', '=', appid), ('app_id.appkey', '=', appkey),
                  ('is_current_version', '=', 'current'),
                  ('is_published', '=', 'published'), ('version_code', '>', params_version)]
        app_version_id = version_obj.search(domain, order='version_code desc', limit=1)
        if not app_version_id:
            re_data.update({"error": [{
                    "code": "300",
                    "message": "没有需要更新的版本",
                    "data": [{
                        "message": "没有需要更新的版本",
                        "debug": "没有需要更新的版本"
                    }]
                }]})
            return re_data
        app_data = [{
            'name': app_version_id.name or '',
            'version': app_version_id.version_code or '',
            "upgrade_text": app_version_id.upgrade_text or '',
            'app_size': "%.2f" % app_version_id.app_size,
            'package_name': app_version_id.package_name or '',
            'app_name': app_version_id.app_id.name or '',
            'create_date':  (app_version_id.create_date + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
            'download_url': app_version_id.qr_code_url or '',
            'is_published': True,
            'is_current_version': True,
            "upgrade_way":  app_version_id.start_cond or '',
            "start_condition": app_version_id.upgrade_style or '',
            "source_version": app_version_id.specify_version_id.version_code or '',
            "inverse_datetime":  (app_version_id.create_date + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') if app_version_id.start_cond=='inverse' else ''
        }]
        re_data.update({"result":app_data})
        return re_data
