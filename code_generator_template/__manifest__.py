# -*- coding: utf-8 -*-
{
    'name': '代码框架生成模块',
    'summary': """
           根据模型名称 生成代码,其中python代码中 生成 类名，xml生成
           表单视图,列表视图,动作 csv生成默认权限
           根据字段值控制form表单编辑与创建按钮
     """,
    'description': """
            根据模型名称 生成代码,其中python代码中 生成 类名，xml生成
            表单视图,列表视图,动作 csv生成默认权限
            根据字段值控制form表单编辑与创建按钮
    """,
    'author': 'melon',
    'website': "http://www.yourcompany.com",
    'license': 'LGPL-3',
    'version': '18.0',
    'category': 'Tools',
    'depends': ['base'],
    "images": ["static/description/img.png"],
    'data': [
        'security/ir.model.access.csv',
        'views/global_module_temp_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
