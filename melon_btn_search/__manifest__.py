# -*- coding: utf-8 -*-
{
    'name': "Melon Btn Search",

    'summary': """
      自定义Dialog,扩展接口搜索功能
       """,
    'description': """
       btn search
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
        'security/ir.model.access.csv',
        'views/demo.xml',
    ],
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'melon_btn_search/static/src/js/btn_search.js'
        ],
        'web.assets_qweb': [
            "melon_btn_search/static/src/xml/base.xml"
        ],
        'web.assets_common': [
            'melon_btn_search/static/src/scss/melon.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
