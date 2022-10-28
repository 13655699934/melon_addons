# -*- coding: utf-8 -*-
{
    'name': "Regular Widget",
    'summary': """Char类型字段的正则表达式""",
    'description': "Regular Expression Widget ",
    'author': "melon",
    'website': "https://hxmelon.com",
    'category': 'Extra Tools',
    'version': '15.0.1',
    'license': 'AGPL-3',
    'depends': ['web'],
    "data": [],
    'images': ['static/description/img_1.png'],
    'assets': {
        'web.assets_backend': [
            'melon_regular_widget/static/lib/jquery.inputmask/jquery.inputmask.bundle.js',
            'melon_regular_widget/static/src/js/fields.js',
            'melon_regular_widget/static/src/js/registry.js'
        ],
        'web.assets_qweb': [
            'melon_regular_widget/static/src/xml/mask.xml'
        ]
    },

    # always loaded

}