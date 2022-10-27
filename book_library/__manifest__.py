# -*- coding: utf-8 -*-
{
    'name': "book_library",

    'summary': """
        Book Library
    """,
    'author': "melon",
    'website': "http://www.hxmelon.com",
    'category': 'Demo',
    'version': '16.0.1',
    'license': 'LGPL-3',
    'images': ["static/description/image.png"],
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
