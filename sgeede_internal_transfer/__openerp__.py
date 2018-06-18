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
	'name': 'SGEEDE Internal Transfer',
	'version': '1.1',
	'category': 'Tools',
	'summary': '''Odoo's enchanced advance stock internal transfer module ''',
	'description': '''Odoo's enchanced advance stock internal transfer module ''',
	'author': 'SGEEDE',
	'website': 'http://www.sgeede.com',
	'depends': ['account', 'stock'],
	'init_xml': [],
	'data': [
		'security/ir.model.access.csv',
		'data/internal_transfer_workflow.xml',
		'wizard/wizard_stock_internal_transfer_view.xml',
		'view/stock_internal_transfer_view.xml',
		'data/ir_sequence.xml',
		'view/res_config_view.xml',
		'view/stock_view.xml',
	],
	'demo_xml': [],
	'installable': True,
	'price': 19.99,
	'currency' : 'EUR',
	'application': True,
	'images': [
		'images/main_screenshot.png',
		'images/sgeede.png'
	]
}