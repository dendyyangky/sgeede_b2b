# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "SGEEDE Date Range",
    "version": "1.0",
    "category": "Custom Development",
    "summary": """SGEEDE Date Range, Add extra feature to your search filter !""",
    "description": """SGEEDE Date Range, Add extra feature to your search filter !""",
    "author": "SGEEDE",
    "website": "http://www.sgeede.com",
    "depends": ['web'],
    "init_xml": [],
    'data': [
        'views/backend.xml'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'price': 14.99,
    'currency': 'EUR',
    'application': True,
    'images': [
        'images/main_screenshot.png',
        'sgeede.png'
    ],
}
