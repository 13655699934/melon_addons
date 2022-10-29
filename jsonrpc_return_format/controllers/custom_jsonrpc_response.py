# -*- coding: utf-8 -*-
import json
import jinja2
import sys
import os
import logging
from odoo.http import JsonRequest, Response
from odoo.tools import date_utils
_logger = logging.getLogger(__name__)


def _json_response(self, result=None, error=None):
    # 自定义odoo接口返回数据格式，获取到参数custom就直接返回json数据，否则就返回默认数据格式
    """
    {
        'jsonrpc': '2.0',
        'id': 12,
        'result': {}
    }
    """
    if self.endpoint and self.endpoint.routing.get('custom'):
        response = {}
        if error is not None:
            response['error'] = error
        if result is not None:
            response = result
    else:
        # odoo返回的默认数据格式
        response = {
            'jsonrpc': '2.0',
            'id': self.jsonrequest.get('id')
        }
        if error is not None:
            response['error'] = error
        if result is not None:
            response['result'] = result

    mime = 'application/json'
    body = json.dumps(response, default=date_utils.json_default)

    return Response(
        body, status=error and error.pop('http_status', 200) or 200,
        headers=[('Content-Type', mime), ('Content-Length', len(body))]
    )


# 重写JsonRequest中的_json_response方法
setattr(JsonRequest, '_json_response', _json_response)
