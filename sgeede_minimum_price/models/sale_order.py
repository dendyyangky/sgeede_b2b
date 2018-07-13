from openerp import api, fields, models, _
from openerp.exceptions import UserError

class SaleOrder(models.Model):
	_inherit = "sale.order"

	@api.multi
	def check_minimum_price(self):
		for line in self.order_line:
			if line.price_unit < line.product_id.minimum_price:
				raise UserError(_("Price is lower than the minimum product price \n Please recheck %s") % (line.product_id.name))
				return False
		return True

#overriding action_confirm to include check_minimum_price
	@api.multi
	def action_confirm(self):
		self.check_minimum_price()
		super(SaleOrder, self).action_confirm()
		 	
