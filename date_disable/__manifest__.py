# -*- coding: utf-8 -*-
{
    'name': 'Date Disable',
    'summary': '日期字段禁用过去日期',
    'category': '通用/tools',
    'description': """日期字段禁用过去日期""",
    'sequence': 666,
    'author': 'melon',
    'website': 'https://hxmelon.com/',
    'depends': ['web'],
    "images": ["static/description/img.png"],
    'version': '15.0.1',
    'data': [
    ],
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'date_disable/static/src/js/disable_date_widget.js',
            'date_disable/static/src/js/disable_datetime_widget.js',
        ],
        'web._assets_primary_variables': [
        ],
        'web._assets_bootstrap': [
        ],
        'web.assets_qweb': [
        ],
        'web.report_assets_common': [
        ],
        'web._assets_common_styles': [
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
