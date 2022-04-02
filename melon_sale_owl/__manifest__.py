# -*- coding: utf-8 -*-
{
    'name': "Melon OWL",

    'summary': """
      MELON SALE OWL
       """,
    'description': """
       MELON SALE OWL
    """,
    'author': "melon",
    "website": "http://www.hxmelon.com",
    "license": "LGPL-3",
    'category': 'owl/page',
    'version': '15.0.1',
    "images": ["static/description/icon.png"],
    'depends': ['base', 'web','sale_management'],
    'data': [
        'views/views.xml'
    ],
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'melon_sale_owl/static/src/js/components/PartnerOrderSummary.js'
        ],
        'web.assets_qweb': [
            "melon_sale_owl/static/src/xml/PartnerOrderSummary.xml"
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
