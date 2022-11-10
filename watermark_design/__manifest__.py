# -*- coding: utf-8 -*-
{
    'name': '自定义PDF和IMG水印',
    'version': '15.0.1',
    'author': 'Melon',
    'category': '通用/水印',
    'website': 'https://hxmelon.com',
    'sequence': 2,
    'currency': "USD",
    'price': 1.88,
    'summary': """
                 WaterMark
                <field name="colorpicker" widget="colorpicker"/>
              """,
    'description': """
        WaterMark Desgin
    """,
    "images": ["static/description/img.png"],
    'depends': ['base',],
    'data': [
        'security/ir.model.access.csv',
        'views/watermark_design_views.xml',
        'views/action_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'watermark_design/static/src/xml/*.xml',
        ],
        'web.assets_backend': [
            '/watermark_design/static/src/css/widget.css',
            '/watermark_design/static/src/lib/bootstrap-colorpicker/css/bootstrap-colorpicker.css',
            '/watermark_design/static/src/js/widget.js',
            '/watermark_design/static/src/lib/bootstrap-colorpicker/js/bootstrap-colorpicker.js'
        ]
    },
    'post_load': None,
    'post_init_hook': None,
    'installable': True,
    'application': True,
    'auto_install': False,
}
