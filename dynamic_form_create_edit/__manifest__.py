# -*- coding: utf-8 -*-
{
    'name': 'Dynamic Form Button',
    'summary': """
           根据控制form表单编辑与创建按钮
     """,
    'description': """
            根据控制form表单编辑与创建按钮
    """,
    'author': 'melon',
    'website': 'http://www.hxmelon.com',
    'license': 'LGPL-3',
    'version': '15.0.0.1',
    'category': 'Tools',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/dynamic_order_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dynamic_form_create_edit/static/src/js/dynamic_form_button.js'
        ],
        'web.assets_qweb': [
        ],
    },
    'images': [
        'static/description/img.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
