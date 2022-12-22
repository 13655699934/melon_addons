import base64
import os
import base64
import logging
import io
import odoo
from odoo import http
from odoo.http import request
from odoo.tools import image_process
import logging

_logger = logging.getLogger(__name__)

ModuleBasedir=os.path.dirname(os.path.dirname(__file__))

'''文件链接预览接口：附件、图片预览'''

class PicUrl(http.Controller):

    @http.route('/ad/image/<int:id>-<string:unique>', type='http', auth="public",crsf=False,cors="*")
    def common_ad_image(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                                  filename_field='name', unique=None, filename=None, mimetype=None,
                                  download=None, width=0, height=0, crop=False, access_token=None,
                                  **kwargs):
        """图片路由地址：
        预览图片可能存在未登陆图片看不到问题：
        """
        if len(unique) < 40:
            return ''
        # other kwargs are ignored on purpose
        return self._common_ad_image(xmlid=xmlid, model=model, id=id, field=field,
                                               filename_field=filename_field, unique=unique, filename=filename,
                                               mimetype=mimetype,
                                               download=download, width=width, height=height, crop=crop,
                                               quality=int(kwargs.get('quality', 0)), access_token=access_token)

    def _common_ad_image(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                                   filename_field='name', unique=None, filename=None, mimetype=None,
                                   download=None, width=0, height=0, crop=False, quality=0, access_token=None,
                                   placeholder='placeholder.png', **kwargs):
        status, headers, image_base64 = request.env['ir.http'].sudo().binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype,
            default_mimetype='image/png', access_token=access_token)
        if status in [301, 304] or (status != 200 and download):
            return request.env['ir.http']._response_by_status(status, headers, image_base64)
        if not image_base64:
            status = 200
            image_base64 = base64.b64encode(self.placeholder(image=placeholder))
            if not (width or height):
                width, height = odoo.tools.image_guess_size_from_field_name(field)
        image_base64 = image_process(image_base64, size=(int(width), int(height)), crop=crop, quality=int(quality))
        content = base64.b64decode(image_base64)
        headers = http.set_safe_image_headers(headers, content)
        response = request.make_response(content, headers)
        response.status_code = status
        return response


    @http.route(['/ad/content/<int:id>-<string:unique>'], type='http', auth="public")
    def ad_content_common(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                          filename=None, filename_field='name', unique=None, mimetype=None,
                          download=None, data=None, token=None, access_token=None, **kw):
        """附件路由地址： 预览图片可能存在未登陆图片看不到问题："""
        if len(unique) < 40:
            return ''
        status, headers, content = request.env['ir.http'].sudo().binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype, access_token=access_token)
        print('status',status)
        print('headers',headers)
        if status != 200:
            return request.env['ir.http']._response_by_status(status, headers, content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)
        if token:
            response.set_cookie('fileToken', token)
        return response




