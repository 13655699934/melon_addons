# -*- coding: utf-8 -*-
{
    'name': "Melon Char Search",

    'summary': """
      扩展文本框搜索功能，可动态搜索数据
       """,
    'description': """
       char search
    """,
    'author': "melon",
    "website": "http://www.hxmelon.com",
    "license": "LGPL-3",
    'category': 'tools/search',
    'version': '15.0.1',
    "images": ["static/description/img_1.png"],
    'depends': ['web'],
    'currency': "USD",
    'price': 6.66,
    'data': [
    ],
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'melon_char_search/static/src/js/char_search.js'
        ],
        'web.assets_qweb': [
            "melon_char_search/static/src/xml/base.xml"
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
