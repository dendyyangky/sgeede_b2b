from openerp import api, fields, models, _
from openerp.exceptions import UserError

class AccountInvoice(models.Model):
	_inherit = "account.invoice"

	@api.multi
	def check_min_price(self):
		for o in self: 
			if o.type == 'out_invoice':
				if not o.invoice_line_ids:
					return False
				for line in o.invoice_line_ids:
					if line.product_id and (line.price_unit < line.product_id.minimum_price):
						raise UserError(_("Price is lower than the minimum product price ! \n Please recheck %s") % (line.product_id.name))
		return True