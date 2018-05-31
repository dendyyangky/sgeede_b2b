# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import odoo
from odoo import fields
from odoo import SUPERUSER_ID
from odoo import tools
from odoo.osv import osv, expression
from odoo.tools.translate import _
from odoo.tools.float_utils import float_round as round

import odoo.addons.decimal_precision as dp

class sale_order(osv.osv):
	_inherit = 'sale.order'

	purchase_id = fields.Many2one('purchase.order', string="Purchase Order ID")
	purchase_line_ids = fields.One2many('purchase.order.line', 'sale_order_id', string="Order Lines")
	