{
    "name": "Export picture to Excel",
    "summary": """Export picture to Excel""",
    "description": """
        Export picture to Excel.
    """,
    "author": "Melon",
    "category": "Tools/Picture Export",
    "website": "http://www.hxmelon.com",
    "version": "15.0.0.1.0",
    "license": "LGPL-3",
    "depends": ["base"],
    "images": ["static/description/image.png"],
    "external_dependencies": {
        "python": ["xlrd"],
    },
    "data": [
        "security/ir.model.access.csv",
        "wizard/export_image_wizard_views.xml",
    ],
}

