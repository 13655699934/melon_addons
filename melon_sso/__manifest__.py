# -*- coding: utf-8 -*-
{
    'name': '单点登录',
    'summary': '单点登录',
    'category': '基础功能',
    'sequence': 666,
    'author': 'melon',
    'website': 'http://www.hxmelon.com',
    'license': 'LGPL-3',
    'version': '15.0.1',
    "images": ["static/description/img_1.png"],
    'depends': ['web'],
    'currency': "USD",
    'price': 6.66,
    'depends': [
        'web', 'base'
    ],
    'version': '0.1',
    'data': [
        'data/ir_config_parameter.xml'
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
                    odoo系统实现单点登陆
                   """,
}
