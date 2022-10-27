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
    # any module necessary for this one to work correctly
    'depends': ['base','mail','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/mrp_order_report.xml',
        'report/report_menu.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'book_library/static/src/js/odoo_form_condition.js'
        ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
