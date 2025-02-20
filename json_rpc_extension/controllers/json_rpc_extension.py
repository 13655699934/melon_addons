# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo.http import JsonRPCDispatcher, Response, request
import json
import werkzeug

def custom_dispatch(self, endpoint, args):
    """
    继承 Odoo 的 JsonRPCDispatcher，解析 `routing` 并传递 `ext`
    """
    try:
        self.jsonrequest = self.request.get_json_data()
        self.request_id = self.jsonrequest.get('id')
    except ValueError:
        werkzeug.exceptions.abort(Response("Invalid JSON data", status=400))
    except AttributeError:
        werkzeug.exceptions.abort(Response("Invalid JSON-RPC data", status=400))

    # 提取参数
    self.request.params = dict(self.jsonrequest.get('params', {}), **args)

    # **获取当前路由的 ext 参数**
    ext_value = endpoint.routing.get('ext', False)  # 这里取出 ext=True 这个参数

    if self.request.db:
        result = self.request.registry['ir.http']._dispatch(endpoint)
    else:
        result = endpoint(**self.request.params)

    # **将 ext 参数传递给 _response**
    return self._response(result, ext=ext_value)

setattr(JsonRPCDispatcher, 'dispatch', custom_dispatch)


def _response(self, result=None, error=None, ext=False):
    """
    统一 Odoo JSON 响应格式，并支持 `ext` 参数
    """
    response = {}
    if ext:  # 如果 `ext=True`，直接返回数据
        if error is not None:
            response = {'jsonrpc': '2.0', 'id': self.request_id, 'error': error}
        elif result is not None:
            response = result
    else:  # 兼容 Odoo 默认返回格式
        response = {'jsonrpc': '2.0', 'id': self.request_id}
        if error is not None:
            response['error'] = error
        if result is not None:
            response['result'] = result

    mime = 'application/json'
    print('======response======',response)
    # body = json.dumps(response)
    body = json.dumps(response, default=str)

    # body = response

    return Response(
        body, status=error and error.pop('http_status', 200) or 200,
        headers=[('Content-Type', mime), ('Access-Control-Allow-Origin', '*'), ('Content-Length', str(len(body)))]
    )

setattr(JsonRPCDispatcher, '_response', _response)
