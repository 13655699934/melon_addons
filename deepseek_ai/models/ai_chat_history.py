from odoo import models, fields,api
import logging
_logger = logging.getLogger(__name__)


class AIChatHistory(models.Model):
    _name = 'ai.chat.history'
    _description = 'AI Chat History'
    _order = 'create_date desc'
    _rec_name = 'message'

    user_id = fields.Many2one('res.users', string='User', required=False)
    model_name = fields.Char(string='AI Model')
    message = fields.Text(string='User Message')
    ai_response = fields.Html(string='AI Response')
    session_id = fields.Char(string='Session ID')  # 支持多会话分组
    create_date = fields.Datetime(string='Create Date')
    annex_file = fields.Binary(string='附件')
    annex_filename = fields.Char(string='附件名称')
    company_id= fields.Many2one('res.company', string='Company')

    @api.model_create_multi
    def create(self, vals):
        records = super(AIChatHistory, self).create(vals)
        return records
