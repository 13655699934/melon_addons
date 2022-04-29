# -*- coding: utf-8 -*-
{
    'name': '导入Excel',
    'summary': """
          导入Excel
       """,
    'author': 'melon',
    "website": "http://www.hxmelon.com",
    "license": "LGPL-3",
    'version': '15.0.1',
    "images": ["static/description/image.png"],
    'category': 'tools/数据导入',
    'description': '数据导入',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/model_views.xml',
        'wizard/import_data_wizard_view.xml',
        'views/actions.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },
}