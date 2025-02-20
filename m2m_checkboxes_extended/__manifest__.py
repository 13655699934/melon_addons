# -*- coding: utf-8 -*-

{
    'name': 'M2m Checkboxes Extended',
    'summary': '多对多选择框自定义列',
    'category': '个性化/排列',
    'sequence': 10,
    'author': 'melon',
    'website': 'http://www.melon.com',
    'depends': ['base', 'web'],
    "images": ["static/description/img.png"],
    'version': '18.0',
    'data': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'm2m_checkboxes_extended/static/src/js/many2many_checkboxes_extended.js',
            'm2m_checkboxes_extended/static/src/xml/many2many_checkboxes_extended.xml',
        ],
    },
    'description': """
在视图定义中,字段的option参数中添加col_count参数
<field name="company_ids" widget="many2many_checkboxes_extended"  options="{'col_count': 4}"/>
""",
}
