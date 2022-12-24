# -*- coding: utf-8 -*-
{
    'name': "melon_mrp_report",
    'summary': """
        MRP打印单
        """,
    'description': """
        MRP打印单
    """,
    'author': "melon",
    'website': "https://www.hxmelon.com",
    'category': 'print',
    'version': '16.0.1',
    "license": "LGPL-3",
    'depends': ['mrp'],
    'images': ["static/description/img_2.png"],
    'data': [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'report/mrp_order_report.xml',
        'report/report_menu.xml'
    ],
    'installable':True, #是否启用安装,通常固定为True
    'auto_install':False,#建库时是否自动安装
    'application':True,#是否为应用程序
}
