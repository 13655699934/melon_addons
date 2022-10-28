# -*- coding: utf-8 -*-
{
    'name': "Dashboard",
    'summary': """
                Dashboard
               """,
    'description': """
        Dashboard
    """,
    'author': "melon",
    'website': "http://www.hxmelon.com",
    'category': 'tools/Dashboard',
    'version': '15.0.0.1',
    'license': 'LGPL-3',
    'currency': "USD",
    'price': 6.66,
    "images": ["static/description/img_4.png"],
    "external_dependencies": {
        "python": [],
    },
    'depends': ['web','base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'melon_dashboard/static/src/js/melon_dashboard.js',
            'melon_dashboard/static/src/js/echarts.min.js',
            'melon_dashboard/static/src/css/dashboard.css',
            'melon_dashboard/static/src/js/china.js',
            'melon_dashboard/static/src/js/echarts.min.js',
            'melon_dashboard/static/src/js/load_pyecharts.js',
            'melon_dashboard/static/src/css/adminlte.min.css',
            'melon_dashboard/static/src/js/theme_dark.js',
            'melon_dashboard/static/src/js/theme_macarons.js',
            'melon_dashboard/static/src/js/theme_vintage.js',
            'melon_dashboard/static/src/js/theme_infographic.js',
            'melon_dashboard/static/src/js/theme_roma.js',
            'melon_dashboard/static/src/js/theme_shine.js',
        ],
        'web.assets_qweb': [
            'melon_dashboard/static/src/xml/melon_dashboard.xml',
            'melon_dashboard/static/src/xml/**/*',
        ],
    }

}
