# -*- coding: utf-8 -*-
{
    'name': "book_library",

    'summary': """
        图书管理模块,Odoo16视图集合
    """,
    'author': "melon",
    'website': "https://www.hxmelon.com",
    'category': 'Demo',
    'version': '16.0.1',
    'license': 'LGPL-3',
    'images': ["static/description/img_2.png"],
    'depends': ['base','mail','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/mrp_order_report.xml',
        'report/report_menu.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
