# -*- coding: utf-8 -*-
{
    'name': 'List View Highlight',
    'version': '15.0',
    'description': """
                    List View Highlight
                    """,
    'summary': """List View Highlight""",
    'category': '通用/列表',
    'license': 'LGPL-3',
    'author': "melon",
    "images": ["static/description/img.png"],
    'website': "http://hxmelon.com",
    'depends': ['web'],
    'data': [
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'melon_row_hlight/static/src/css/style.css',
            'melon_row_hlight/static/src/js/web.js',
        ],

        'web.assets_qweb': [
        ],
    }
}
