from openerp.osv import osv, fields, expression
from openerp import workflow
from openerp.tools.translate import _

class sale_order(osv.osv):
	_inherit = 'sale.order'

	def min_price_check(self, cr, uid, ids, context):
		context = context or {}
		for order in self.browse(cr, uid, ids):
			print len(order.order_line)
			for line in order.order_line:
				if line.product_id and (line.price_unit < line.product_id.minimum_price):
					raise osv.except_osv(_('Error'), _("Price is lower than the minimum product price! \n Please recheck %s") % (line.product_id.name))
					return False
		return True

#call min price check and then call the parent functions
	def action_button_confirm(self, cr, uid, ids, context=None):
		if self.min_price_check(cr, uid, ids, context):
			super(sale_order, self).action_button_confirm(cr, uid, ids, context=None)
