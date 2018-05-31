# -*- coding: utf-8 -*-
{
    'name': "Back to Back Purchase Order from Sales order",

    'summary': """Generate Back to Back Purchase Order in Sale Order""",

    'description': """
    Generate Back to Back Purchase Order in Sale Order
        
    """,
    
    'author': "SGEEDE",
    'website': "http://www.sgeede.com",
    'category': 'Tools',
    'version': '2',
    'depends': ['base','sale','purchase'],
    'data': [
        'wizard/back_to_back_order_view.xml',
        'views/sale_view.xml',
        # 'security/ir.model.access.csv',  
    ],
    'demo': [],
    'installable': True,
    'active': False,
    'certificate': '',
    'price': 9.99,
    'currency': 'EUR',
    'images': ['images/main_screenshot.png',
    'images/sgeede.png'],
}