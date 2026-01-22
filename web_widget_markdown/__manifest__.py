{
    "name": "Widget Text Markdown",
    "version": "18.0",
    "author": "melon, ",
    "description":
        """
           Markdown格式插件
           <field name="ai_response" widget="bootstrap_markdown"/>
        """,
    "category": "Tools",
    "license": 'LGPL-3',
    'website': 'https://www.zjdtcloud.com/',
    "summary": "Widget adds markdown support",
    "images": ["static/description/img2.png"],
    "depends": ["web", "base"],
    "data": [],
    "installable": True,
    "auto_install": False,
    "application": True,
    "assets": {
        "web.assets_backend": [
            # CSS
            "web_widget_markdown/static/src/css/web_widget_text_markdown.css",
            # Component
            "web_widget_markdown/static/src/js/web_widget_text_markdown.js",
            # Dependencies
            "/web/static/src/views/fields/text/text_field.js",
        ],
    },
}
