# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
	'name': 'SGEEDE Minimum Price Module',
	'version': '1.0',
	'category': 'Tools',
	'summary': """Lock and control your minimum sale price to POS, Sales Order and Invoice""",
	'description': """Lock and control your minimum sale price to POS, Sales Order and Invoice""",
	'author': "SGEEDE",
	'website': "http://www.sgeede.com",
	'depends': ['sale', 'point_of_sale'],
	'init_xml': [],
	'update_xml': [
		'views/product_extend_view.xml',
		'views/point_of_sale_extend.xml',
		'views/account_invoice_workflow.xml',
	],
	'qweb': ['static/src/xml/*.xml'],
	'demo_xml': [],
	'installable': True,
    'active': False,
	'price': 9.99,
	'certificate': '',
	'currency': 'EUR',
	'images': [
		'images/sgeede.png',
		'images/main_screenshot.png'
	],
}