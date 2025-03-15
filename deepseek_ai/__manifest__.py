# -*- coding: utf-8 -*-
{
    'name': "DeepSeek AI",
    'summary': "DeepSeek Intergration with Odoo",
    'description': """
         将DeepSeek与Odoo集成可以增强您的ERP系统的先进人工智能能力
    """,

    'author': "Melon",
    'website': "http://www.hxmelon.com/",
    'version': '0.1',
    'external_dependencies': {
        'python': ['openai'],
    },
    'depends': ['base','base_setup'],
    'images': ['static/description/chat.png'],
    'data': [
        'data/ir_config_parameter.xml',
        'security/base_groups.xml',
        'security/base_security.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/action_views.xml',
        'views/ai_chat_history_views.xml',
        'views/menu_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'deepseek_ai/static/src/xml/deepseek_ai_tags.xml',
            'deepseek_ai/static/src/js/deepseek_ai_tags.js',
        ],
        'qweb': [
        ],
    },
    'license': 'GPL-3',
}

