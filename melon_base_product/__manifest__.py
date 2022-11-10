
{
    "name": "Product Base",
    "summary": "产品模块继承 通用字段扩展",
    "version": "15.0.1.0.0",
    "category": "product",
    "website": "http://www.hxmelon.com",
    "author": "Melon",
    "license": "LGPL-3",
    "installable": True,
    "depends": ['product','sale','purchase','stock'],
    "images": ["static/description/img.png"],
    "maintainers": [],
    "data": [
        'security/ir.model.access.csv',
        'views/product_base_views.xml',
        'views/purchase_base_views.xml',
        'views/sale_base_views.xml',
        'views/stock_base_views.xml',
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
}
