from odoo import fields, models
from odoo.osv import osv
from odoo.tools.translate import _ 
import odoo.addons.decimal_precision as dp

class purchase_order_line(osv.osv):
	_inherit = "purchase.order.line"

	sale_order_id = fields.Many2one('sale.order', string="Order")