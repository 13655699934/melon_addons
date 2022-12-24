import json
import logging
import time
from odoo import models
from odoo.exceptions import UserError
from odoo.http import request as http_request
from odoo.tools.config import config

_logger = logging.getLogger('monitoring.http.requests')


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        """
        路由拦截
        """
        begin = time.time()
        response = super(IrHttp, cls)._dispatch()
        end = time.time()
        if (not cls._monitoring_blacklist(http_request) and
                cls._monitoring_filter(http_request)):
            cls._monitoring_info(http_request, response, begin, end)
        return response

    @classmethod
    def _monitoring_blacklist(cls, request):
        """
        监控路径过滤 增、删、改
        """
        path_info = request.httprequest.environ.get('PATH_INFO')
        if path_info.endswith(('/write', '/create', '/unlink', '/xlsx', '/report/download', '/base_import/set_file')):
            return False
        return True

    @classmethod
    def _monitoring_filter(cls, _):
        return True

    @classmethod
    def _monitoring_info(cls, request, response, begin, end):
        AuditLog = request.env['audit.logs']
        Model = request.env['ir.model']
        User = request.env['res.users']

        path = request.httprequest.environ.get('PATH_INFO')
        info = {
            # timing
            'start_time': time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.gmtime(begin)),
            'duration': end - begin,

            # HTTP things
            'method': request.httprequest.method,
            'url': request.httprequest.url,
            'ipaddress': request.httprequest.remote_addr,
            'path': path,
            'content_type': request.httprequest.environ.get('CONTENT_TYPE'),
            'user_agent': request.httprequest.environ.get('HTTP_USER_AGENT'),
            # Odoo things
            'db': None,
            'user_id': request.uid,
            'login': None,
            'server_environment': config.get('running_env'),
            'model': None,
            'model_method': None,
            'workflow_signal': None,
            # response things
            'response_status_code': None,
            'result': '操作成功',
        }
        if hasattr(response, 'status_code'):
            info['status_code'] = response.status_code
            if response.status_code != 200:
                info['result'] = '操作失败'
                info['response_status_code'] = response.status_code
        if hasattr(request, 'session'):
            info.update({
                'login': request.session.get('login'),
                'db': request.session.get('db'),
            })
        if hasattr(request, 'params'):
            info.update({
                'model': request.params.get('model'),
                'model_method': request.params.get('method'),
                'workflow_signal': request.params.get('signal'),
            })
        if path.endswith(('xlsx')):
            info.update({
                'model': json.loads(request.params.get('data')).get('model'),
                'model_method': 'export',
            })
        try:
            if path.endswith(('/report/download')):
                info.update({
                    'model_method': 'report',
                })
            if path.endswith(('/base_import/set_file')):
                info.update({
                    'model_method': 'import',
                })
            model_id = Model.sudo().search([('model', '=', info.get('model', False))])
            user_id = User.sudo().search([('id', '=', int(info.get('user_id', False)))])
            model_method = info.get('model_method')
            
            params = {
                "name": "操作名称未命名",
                "model_method": info.get('model_method'),
                "ipaddress": info.get('ipaddress'),
                "url": info.get('url'),
                "result": info.get('result'),
                'params': request.params.get('data') or request.params,
            }
            if model_method == 'write':
                params.update({"name": "修改"})
            if model_method == 'create':
                params.update({"name": "新增"})
            if model_method == 'unlink':
                params.update({"name": "删除"})
            if model_method == 'xlsx':
                params.update({"name": "导出xlsx"})
            if model_method == 'report':
                params.update({"name": "预览打印"})
            if model_method == 'import':
                params.update({"name": "文件导入"})
            if model_method == 'export':
                params.update({"name": "文件导出"})
            if model_id:
                params.update({"model_id": model_id.id})
            if user_id:
                params.update({"user_id": user_id.id})
            AuditLog.create(params)
            return info
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '操作失败',
                    'type': 'warning'
                },
            }


    @classmethod
    def _monitoring_log(cls, info):
        print(json.dumps(info))
