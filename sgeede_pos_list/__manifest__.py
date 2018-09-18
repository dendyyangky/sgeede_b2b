# -*- encoding : utf-8 -*-
{
    'name': 'SGEEDE POS List',
    'version': '1.0',
    'category': 'Custom Development',
    'summary': 'Allow list view in Point of Sale',
    'description': """
        Allow list view in Point of Sale.
    """,
    'author': "SGEEDE",
    'website': "http://www.sgeede.com",
    'depends': ['point_of_sale'],
    'data': [
        'views/sgeede_pos_list.xml',
        'views/pos_config_view.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'price': 9.99,
    'currency': 'EUR',
    'license': 'LGPL-3',
    'images': [
        'images/main_screenshot.png',
        'images/sgeede.png'
    ]
}