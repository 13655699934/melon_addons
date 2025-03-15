# -*- coding: utf-8 -*-
import os
import odoo
from odoo import http, _
from jinja2 import Environment, FileSystemLoader
import logging
from datetime import datetime, timedelta
_logger = logging.getLogger(__name__)
from odoo.http import request
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/static/templates/")
env = Environment(loader=templateLoader)
from odoo.http import Response
from openai import OpenAI
class AnalysisReportApi(http.Controller):

    @http.route('/deepseek/ai/chat/api', type='http', auth="public")
    def deepseek_ai_chat_api(self, **kw):
        """

        :param kw:
        :return:
        """
        cr, uid, context, pool = request.cr, odoo.SUPERUSER_ID, request.context, request.env
        api_url = request.env['ir.config_parameter'].sudo().get_param('deepseek_ai.ai_chat_url')
        api_key =request.env['ir.config_parameter'].sudo().get_param('deepseek_ai.ai_chat_api_key')
        ai_model = request.env['ir.config_parameter'].sudo().get_param('deepseek_ai.ai_chat_model')
        values = {'api_url': api_url,'api_key':api_key,'ai_model':ai_model}
        try:
            template = env.get_template('zh_CN/chat_openroute_stream.html')
            html = template.render(values)
        except IOError:
            template = env.get_template('zh_CN/404.html')
            html = template.render(values)
        return html

    @http.route('/ai/stream_chat', type='http', auth='public', cors='*')
    def ai_stream_chat(self, **kwargs):
        user_id = request.session.uid
        user_message = kwargs.get('user_message')
        file_content = kwargs.get('file_content', '')
        api_url = request.env['ir.config_parameter'].sudo().get_param('deepseek_ai.ai_chat_url')
        api_key = request.env['ir.config_parameter'].sudo().get_param('deepseek_ai.ai_chat_api_key')
        ai_model = request.env['ir.config_parameter'].sudo().get_param('deepseek_ai.ai_chat_model')
        # ✅ 初始化 OpenAI Client（基于 OpenRouter）
        client = OpenAI(
            base_url=api_url,
            api_key=api_key
        )

        # ✅ 查询最近 10 条对话历史，按时间倒序
        # history_records = request.env['ai.chat.history'].sudo().search(
        #     [('user_id', '=', user_id)], order='create_date desc', limit=10
        # )
        # # ✅ 组装历史消息
        # history_messages = []
        # for record in reversed(history_records):  # 旧的消息先加入
        #     history_messages.append({"role": "user", "content": record.message})
        #     history_messages.append({"role": "assistant", "content": record.ai_response})

        # ✅ 组装最终对话信息
        messages = [{"role": "user", "content": file_content[:5000]},
                    {"role": "user", "content": user_message}]
        # ✅ 定义 SSE 事件流
        def event_stream():
            try:
                # ✅ 发起流式请求
                completion = client.chat.completions.create(
                    model=ai_model,
                    messages=messages,
                    stream=True,  # 流式返回！
                    extra_headers={
                        "HTTP-Referer": "DeepSeek R1",  # 自定义
                        "X-Title": "Odoo AIChat"  # 自定义
                    }
                )
                # ✅ 遍历生成流
                response_text = ""  # 用于存储最终 AI 响应
                for chunk in completion:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        response_text += delta.content
                        # 发送数据（SSE 格式）
                        yield f"data: {chunk.model_dump_json()}\n\n"
                # ✅ 结束信号
                yield "data: [DONE]\n\n"
            except Exception as e:
                # 捕获异常
                yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
        return Response(event_stream(), content_type='text/event-stream')

    @http.route('/ai/history', type='json', auth='public')
    def get_chat_history(self, period=None, **kwargs):
        user_id = request.session.uid
        domain = [('user_id', '=', user_id)]
        from_date = datetime.today() - timedelta(days=7)
        domain += [('create_date', '>=', from_date)]
        history_records = request.env['ai.chat.history'].sudo().search(domain, limit=50)
        result = [{
            'id': rec.id,
            'message': rec.message,
            'ai_response': rec.ai_response,
            'model': rec.model_name,
            'create_date': rec.create_date.strftime('%Y-%m-%d %H:%M')
        } for rec in history_records]
        return {'history': result}

    @http.route('/ai/create_chat_history', type='json', auth='none', csrf=False)
    def create_chat_history(self, **kw):
        user_id = request.session.uid
        user = request.env['res.users'].sudo().browse(request.session.uid)
        data = request.get_json_data()
        user_message = data.get('user_message')
        ai_message = data.get('ai_message')
        annex_file = data.get('annex_file')  # base64 字符串
        annex_filename = data.get('annex_filename')
        ai_model = request.env['ir.config_parameter'].sudo().get_param('deepseek_ai.ai_chat_model')
        if not user_message or not ai_message:
            return {'success': False, 'error': '用户消息或AI消息为空'}
        try:
            request.env['ai.chat.history'].sudo().create({
                'message': user_message,
                'ai_response': ai_message,
                'model_name': ai_model,
                'annex_file': annex_file,
                'annex_filename': annex_filename,
                'user_id': user_id,
                'company_id': user.company_id.id,
            })
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}





