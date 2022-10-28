# -*- coding: utf-8 -*-
{
    'name': 'Base Extend',
    'summary': '主题色调全局样式修改',
    'category': '通用/基础扩展',
    'description': """全局样式修改""",
    'sequence': 666,
    'author': 'melon',
    'website': 'http://hxmelon.com/',
    'depends': ['base', 'web'],
    "images": ["static/description/img.png"],
    'version': '15.0.1',
    'data': [
    ],
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'base_extend/static/src/scss/extend_form_view_extra.scss',
            'base_extend/static/src/scss/form_renderer.scss',
        ],
        'web._assets_primary_variables': [
            'base_extend/static/src/scss/extend_main.scss',
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
