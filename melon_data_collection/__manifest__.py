# -*- coding: utf-8 -*-
{
    'name': 'Information Acquisition',
    'summary': '信息采集',
    'category': '信息采集/基础功能',
    'sequence': 100,
    'author': 'melon',
    'website': 'https://www.hxmelon.com/',
    'depends': ['base', 'mail', 'web'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """信息采集""",
    'license': 'LGPL-3',
    'version': '15.0.1',
    "images": ["static/description/images.png"],
    'data': [
        'security/ir.model.access.csv',
        "wizard/talent_inform_import_wizard_views.xml",
        'views/talent_base_inform.xml',
        'views/actions.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'melon_data_collection/static/src/js/extend_tree_button.js',
        ],
        'web.assets_qweb': [
            'melon_data_collection/static/src/xml/**/*',
        ],
    },
}
