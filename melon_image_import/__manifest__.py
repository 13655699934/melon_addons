{
    "name": "Picture import",
    "summary": """Picture import""",
    "description": """
        Import pictures into package by batch compression.
    """,
    "author": "Melon",
    "category": "Tools/Picture import",
    "website": "http://www.hxmelon.com",
    "version": "15.0.0.1.0",
    "license": "LGPL-1",
    "depends": ["base"],
    "images": ["static/description/image.png"],
    "external_dependencies": {
        "python": [],
    },
    "data": [
        "security/ir.model.access.csv",
        "wizard/import_image_wizard_views.xml",
    ],
}
