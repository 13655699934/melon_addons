{
    "name": "Export picture to Excel",
    "summary": """Export picture to Excel""",
    "description": """
        图片导出至Excel单元格中.
    """,
    "author": "Melon",
    "category": "Tools/Picture Export",
    "website": "http://www.hxmelon.com",
    "version": "15.0.0.1.0",
    "license": "LGPL-3",
    "depends": ["base"],
    "images": ["static/description/img_1.png"],
    "external_dependencies": {
        "python": ["xlrd"],
    },
    "data": [
        "security/ir.model.access.csv",
        "wizard/export_image_wizard_views.xml",
    ],
}

