# -*- coding: utf-8 -*-
{
    'name': 'melon_echarts',
    'version': '15.0',
    'author': "melon",
    'website': 'https://www.hxmelon.com',
    'summary': '集成pyecharts',
    'description': """pyecharts""",
    'license': 'LGPL-3',
    'images': ["static/description/img_2.png"],
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'data/demo_data_views.xml',
        'data/ir_config_parameter_data.xml',
        'views/data_template_view.xml',
    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'application': True,
    'external_dependencies': {
        'python': ['pyecharts']
    },
    'assets': {
        'web.assets_backend': [
            'melon_pyecharts/static/src/js/echarts.min.js'
        ],
        'web.assets_qweb': []
    }

}
