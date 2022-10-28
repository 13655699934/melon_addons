# -*- coding: utf-8 -*-
{
    'name': 'QR Code',
    'summary': """
           二维码生成器
     """,
    'description': """
            二维码生成器
    """,
    'author': 'melon',
    'website': 'http://www.hxmelon.com',
    'license': 'LGPL-3',
    'version': '15.0.0.1',
    'category': 'Tools',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_views.xml',
        'views/qr_code_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },
    'images': [
        'static/description/img_2.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
