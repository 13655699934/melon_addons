# -*- coding: utf-8 -*-
{
    'name': '附件打包',
    'summary': u'附件打包',
    'category': u'通用/附件打包',
    'description': u"""
                     附件打包下载 
                    """,
    'sequence': 90,
    'author': 'Melon',
    'website': 'http://hxmelon.com/',
    'depends': ['base', 'mail'],
    'version': '15.0.1',
    "license": "LGPL-3",
    "images": ["static/description/img.png"],
    'data': [
        'security/ir.model.access.csv',
        'views/demo_views.xml',
        'views/action_views.xml',
        'views/menu_views.xml',
     ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
