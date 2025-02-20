# -*- coding: utf-8 -*-

{
    "name": "操作日志",
    "version": "18.0",
    "sequence": 100,
    "category": "Tools",
    "license": 'LGPL-3',
    "description": """该模块允许管理员跟踪用户的使用系统的所有操作过程""",
    'author': 'melon',
    'website': "http://www.yourcompany.com",
    "images": ["static/description/img.png"],
    "depends": [
        'base',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/audit_logs_view.xml',
        'views/audit_login.xml',
        'views/audit_ip_whitelist.xml',
        'views/menu_item.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
