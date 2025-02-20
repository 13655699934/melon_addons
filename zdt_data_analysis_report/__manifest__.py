# -*- coding: utf-8 -*-
{
    'name': '数据分析报表',
    'description': '数据分析报表',
    'author': "melon",
    'category': 'tools',
    'version': '18.0',
    'website': "www.hxmelon.com",
    'depends': ['base', 'hr','web'],
    'application': True,
    "images": ["static/description/img.png"],
    'data': [
        'security/ir.model.access.csv',
        'views/data_analysis_views.xml',
        'views/menu_view.xml'
    ],
    'css': [
    ],
    'qweb': [
    ],
    'demo': [

    ],
    'assets': {
        'web.assets_backend': [
            'zdt_data_analysis_report/static/src/xml/data_analysis_report.xml',
            'zdt_data_analysis_report/static/src/js/data_analysis_report.js',
        ],
        'qweb': [
        ],
    },
    'license': 'LGPL-3',
}