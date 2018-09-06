# -*- coding: utf-8 -*-
{
    'name': 'SGEEDE POS Lock',
    'version': '1.0',
    'category': 'Custom Development',
    'summary': 'Allow users to lock their Point of Sale with password',
    'description': """
        Allow users to lock their Point of Sale with password.
    """,
    'author': "SGEEDE",
    'website': "http://www.sgeede.com",
    'depends': ['point_of_sale'],
    'data': [
        'views/sgeede_pos_lock.xml'
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'price': 9.99,
    'currency': 'EUR',
    'auto_install': False,
    'images': [
        'images/main_screenshot.png',
        'images/sgeede.png'
    ]
}