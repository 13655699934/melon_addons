# -*- coding: utf-8 -*-
{
    'name': 'APK应用发布',
    'summary': """
           APK应用发布
     """,
    'description': """
            APK应用发布
    """,
    'author': 'melon',
    'website': 'https://www.hxmelon.com',
    'license': 'LGPL-3',
    'version': '15.0.0.1',
    'category': 'Tools',
    'currency': "USD",
    'price': 0.88,
    'depends': ['web','mail'],
    "images": ["static/description/img_1.png"],
    'data': [
        'security/ir.model.access.csv',
        'data/application_content_type.xml',
        'data/ir_config_parameter.xml',
        'views/melon_application_manager_views.xml',
        'views/melon_application_version_views.xml',
        'views/melon_ir_ui_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
