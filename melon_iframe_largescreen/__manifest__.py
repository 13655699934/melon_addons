{
    "name": "Large Screen",
    "summary": """Large Screen""",
    "description": """
        H5 Large visual screen.
    """,
    "author": "Melon",
    "category": "Tools/Large visual screen",
    "website": "http://www.hxmelon.com",
    "version": "15.0.0.1.0",
    "license": "LGPL-3",
    "depends": ["base"],
    "images": ["static/description/img.png"],
    "external_dependencies": {
        "python": [],
    },
    "data": [
        'views/actions.xml',
        'views/menu.xml'
    ],
    'assets': {
            'web.assets_backend': [
                '/melon_iframe_largescreen/static/src/js/melon_iframe_report.js'
            ],
            'web.assets_qweb': [
                '/melon_iframe_largescreen/static/src/xml/melon_iframe_report_views.xml'
            ],
        }
}

