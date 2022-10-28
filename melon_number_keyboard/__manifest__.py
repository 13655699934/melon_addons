# -*- coding: utf-8 -*-
{
    'name': "melon_number_keyboard",
    'summary': """
            number keyboard
       """,
    'description': """
      number keyboard
    """,
    'author': "melon",
    "license": "LGPL-3",
    'category': 'tools/search',
    'version': '15.0.1',
    "images": ["static/description/img_2.png"],
    'depends': ['web'],
    'data': [
        "security/ir.model.access.csv",
        "views/keyboard_views.xml",
        "wizards/keyword_wizard_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'melon_number_keyboard/static/src/css/keyboard_bass.css',
            'melon_number_keyboard/static/src/js/number_keyboard.js',
            'melon_number_keyboard/static/src/js/integer_keyboard.js'
        ],
        'web.assets_qweb': [
            "melon_number_keyboard/static/src/xml/base.xml"
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
