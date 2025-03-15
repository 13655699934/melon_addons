from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ai_chat_url = fields.Char(string="API Key", config_parameter="deepseek_ai.ai_chat_url")
    ai_chat_api_key = fields.Char(string="API Key", config_parameter="deepseek_ai.ai_chat_api_key")
    ai_chat_model = fields.Selection(selection=[('deepseek/deepseek-r1', 'Deepseek-R1'),
                                              ('deepseek/deepseek-r1-distill-llama-8b', 'Deepseek-llama-8b'),
                                              ('deepseek/deepseek-r1-distill-llama-70b', 'Deepseek-llama-70b'),
                                              ('deepseek/deepseek-r1-distill-llama-70b:free', 'Deepseek-llama-70b:free'),
                                              ('deepseek/deepseek-r1-distill-qwen-14b', 'Deepseek-qwen-14b')
                                           ],
                                   string="AI模型",
                                   help="选择你的模型",
                                   config_parameter="deepseek_ai.ai_chat_model")
