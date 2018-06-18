# -*- encoding: utf-8 -*-
{
    'name': 'SGEEDE Internal Transfer',
    'version': '1.1',
    'category': 'Tools',
    'summary': '''Odoo's enchanced advance stock internal transfer module''',
    'description': '''Odoo,s enchanced advance stock internal transfer module''',
    'author': 'SGEEDE',
    'website': 'http://www.sgeede.com',
    'depends': ['account','stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_stock_internal_transfer_view.xml',
        'views/stock_internal_transfer_view.xml',
        'data/ir_sequence.xml',
        'views/stock_view.xml',
        'views/res_config_view.xml',
    ],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'price': 19.99,
    'currency': 'EUR',
    'images': [
        'images/main_screenshot.png',
        'images/sgeede.png'
    ],
}