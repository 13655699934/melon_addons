# -*- coding: utf-8 -*-
{
    'name': 'Field Masking Widget',
    'version': '18.0.1.0.0',
    'category': 'Web',
    'summary': '字段脱敏显示挂件 - 支持手机号、身份证、银行卡等',
    'description': """
Field Masking Widget
====================

保护用户隐私的字段显示挂件。

功能特性
--------

- 📱 手机号脱敏：``138****1234``
- 🪪 身份证脱敏：``340***********1234``
- 💳 银行卡脱敏：``6222 **** **** 1234``
- 📧 邮箱脱敏：``abc***@gmail.com``
- 👤 姓名脱敏：``张*``、``李**``
- 🔧 自定义脱敏规则：支持自定义保留前后位数

使用方法
--------

在视图 XML 中使用：

.. code-block:: xml

    <field name="mobile" widget="masked_field"/>
    <field name="id_card" widget="masked_field" mask_type="id_card"/>
    <field name="email" widget="masked_field" mask_type="email"/>

高级选项
--------

- ``mask_type``：``phone`` / ``id_card`` / ``bank_card`` / ``email`` / ``name`` / ``custom``
- ``mask_char``：脱敏字符（默认：``*``）
- ``mask_start``：保留前 N 位（仅 ``custom`` 生效）
- ``mask_end``：保留后 N 位（仅 ``custom`` 生效）
- ``show_on_hover``：鼠标悬停显示完整内容（默认：``True``）

特色功能
--------

- 🖱️ 鼠标悬停显示完整内容
- 📋 双击复制到剪贴板
- 🎨 更友好的视觉效果
""",
    'author': 'hsx',
    'website': 'https://www.zjdtcloud.com/',
    'license': 'LGPL-3',
    'depends': ['web'],
    'images': ['static/description/img_1.png'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'web_field_mask/static/src/js/masked_field_widget.js',
            'web_field_mask/static/src/xml/masked_field_widget.xml',
            'web_field_mask/static/src/scss/masked_field.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
