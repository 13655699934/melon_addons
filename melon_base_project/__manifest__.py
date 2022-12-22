# -*- coding: utf-8 -*-
{
    "name": "Project Base",
    "summary": "Add Project",
    "version": "16.0.1.0.0",
    "category": "base",
    "website": "https://www.hxmelon.com",
    "author": "Melon",
    "license": "LGPL-3",
    "installable": True,
    "depends": ['product','sale','purchase','project','stock','account','sale_management'],
    "maintainers": [],
    'images': ["static/description/img_2.png"],
    "data": [
        'security/account_groups.xml',
        'data/ir_sequence_views.xml',
        'security/ir.model.access.csv',
        'views/product_base_views.xml',
        'views/purchase_base_views.xml',
        'views/sale_base_views.xml',
        'views/stock_base_views.xml',
        'views/stock_move_line_views.xml',
        'views/stock_value_layer_views.xml',
        'views/menus.xml',
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
}
