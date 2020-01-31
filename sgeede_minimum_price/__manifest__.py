# -*- encoding: utf-8 -*-
{
	'name': "SGEEDE Minimum Price Module",
	'version': '1.0',
	'category': 'Tools',
	'summary': """Lock and control your minimum sale price to POS, Sales Order and Invoice""",
	'description': """Lock and control your minimum sale price to POS, Sales Order and Invoice""",
	'author': 'SGEEDE',
	'website': 'http://www.sgeede.com',
	'depends': ['sale'],
	'data': [
		'views/product_view.xml',
		'views/point_of_sale.xml',
	],
	'qweb': ['static/src/xml/*.xml'],
	'demo_xml': [],
	'installable': True,
	'active': False,
	'price': 9.99,
	'currency': "EUR",
	'license': 'LGPL-3',
	'images': [
		'images/main_screenshot.png',
		'images/sgeede.png'
	],
}