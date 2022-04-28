# -*- coding: utf-8 -*-
{
    "name": "导入Excel",
    "summary": """
          导入Excel
       """,
    "website": "http://www.hxmelon.com",
    "license": "LGPL-3",
    "version": "15.0.1",
    "category": "tools/数据导入",
    "description": "数据导入",
    "author": "melon",
    "depends": ["base"],
    "images": ["static/description/image.png"],
    "data": [
        "security/ir.model.access.csv",
        "views/model_views.xml",
        "wizard/import_data_wizard_view.xml",
        "views/actions.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
        ],
        "web.assets_qweb": [
        ],
    },
    "images": [
    ],
}
