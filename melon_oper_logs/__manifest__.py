# -*- coding: utf-8 -*-
{
    "name": "日志追踪",
    "version": "0.1",
    "sequence": 100,
    "category": "Tools",
    "license": 'LGPL-3',
    'version': '15.0.1',
    "description": """该模块允许管理员跟踪每个用户的操作系统的所有对象.""",
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
