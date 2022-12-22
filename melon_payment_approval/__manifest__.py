
{
    "name": "Payment Approval",
    "summary": "Payment Approval",
    "version": "16.0.1",
    "category": "Approval",
    "website": "https://www.hxmelon.com",
    "author": "Melon",
    "license": "LGPL-3",
    "installable": True,
    "depends": ['account'],
    'images': ["static/description/img_3.png"],
    "maintainers": [],
    "data": [
        'security/account_groups.xml',
        'security/ir.model.access.csv',
        'views/account_base_views.xml',
        'views/account_payment_views.xml',
        'views/menus.xml',
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
}
