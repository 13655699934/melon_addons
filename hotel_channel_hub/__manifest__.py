# -*- coding: utf-8 -*-
{
    'name': 'Hotel Management and Channel Aggregation System',
    'version': '18.0.1.0.0',
    'category': 'Industries',
    'summary': '酒店管理、房态管理、订单管理、多渠道聚合、API接口',
    'description': """
        酒店管理与渠道聚合系统
        ========================
        * 酒店、房型、房间管理
        * 订单管理（线上线下）
        * 多渠道聚合与API接口
        * 库存与价格管理
        * 数据看板与消息面板
        * 权限控制与审计日志
        * 支持多公司、多酒店
    """,
    'author': 'Melon',
    'website': 'https://www.zjdtcloud.com/',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
    ],
    'data': [
        # Security
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        
        # Data
        'data/sequence.xml',
        'data/cron.xml',
        
        # Views
        'views/hotel_views.xml',
        'views/room_type_views.xml',
        'views/room_views.xml',
        'views/channel_views.xml',
        'views/order_views.xml',
        'views/availability_views.xml',
        'views/sync_log_views.xml',
        'views/dashboard_views.xml',
        'views/hotel_date_center.xml',
        'views/menu_views.xml',  # 菜单放在最后，确保所有action都已定义
        
        # Reports
        'report/order_report.xml',
        'report/order_report_template.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hotel_channel_hub/static/src/xml/hotel_data_center.xml',
            'hotel_channel_hub/static/src/js/hotel_data_center.js',
        ],
        'web.assets_frontend': [
        ],
    },
    'images': ['static/description/image.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}

