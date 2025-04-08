# -*- coding: utf-8 -*-
{
    'name': "Portal 任务管理",
    'summary': """task card management""",
    'description': """
        Portal 任务管理
    """,
    'author': "melon",
    'website': "https://www.hxmelon.com/",
    'category': 'tools',
    'version': '18.0',
    "images": ["static/img/img.png"],
    'depends': [
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/inhert_home_portal.xml',
        'views/task_card_portal_templates.xml',
        'views/portal_my_home.xml',
        'views/portal_task_order_detail.xml',
        'views/portal_task_edit_views.xml',
        'views/task_card_order_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    "license": "AGPL-3",
}