# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "SGEEDE Infinite Scroll",
    "version": "1.0",
    "category": "Custom Development",
    "summary": """SGEEDE Infinite Scroll. Allow infinite scroll in Products without using pagination anymore.""",
    "description": """SGEEDE Infinite Scroll. Allow infinite scroll in Products without using pagination anymore.""",
    "author": "SGEEDE",
    "website": "http://www.sgeede.com",
    "depends": ['website', 'website_sale'],
    "init_xml": [],
    'data': [
        'views/frontend.xml',
        'views/templates.xml'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'price': 14.99,
    'currency': 'EUR',
    'application': True,
    'images': [
        'images/icon.png',
    ],
}

