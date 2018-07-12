from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	@api.multi
	def check_min_price(self):
		for order in self:
			for line in order.order_line:
				if line.product_id and (line.price_unit < line.product_id.minimum_price):
					raise UserError(_("Price is lower than the minimum product price !  \n Please recheck %s") % (line.product_id.name))
					return False
		return True

#extend action_confirm to include check_min_price
	@api.multi
	def action_confirm(self):
		self.check_min_price()
		super(SaleOrder, self).action_confirm()