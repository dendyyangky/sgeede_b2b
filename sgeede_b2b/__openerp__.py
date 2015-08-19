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
    'name': 'Back To Back Purchase Order from Sales order',
    'version': '1.0',
    'category': 'Tools',
    'summary': """Generate Back to Back Purchase order in Sale order""",
    'description': """Generate Back to Back Purchase order in Sale order""",
    'author': 'SGEEDE',
    'website': 'http://www.sgeede.com',
    'depends': ['base','sale','purchase'],
    'init_xml': [],
    'update_xml': [
         'wizard/back_to_back_order.xml',
         'sale_view.xml',
         
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'certificate': '',
    'price': 14.99,
    'currency': 'EUR',
    'images': ['images/main_screenshot.png',
    'images/sgeede.png'

    ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
