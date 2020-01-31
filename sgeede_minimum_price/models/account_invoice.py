from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountInvoice(models.Model): 
	_inherit = 'account.invoice'
	@api.multi
	def check_minimum_price(self):
		for line in self.invoice_line_ids:
			if line.product_id and (line.price_unit < line.product_id.minimum_price):
				raise UserError(_("Price is lower than the minimum product price! \n Please recheck %s") % (line.product_id.name))
				return False
		return True

	@api.multi
	def action_invoice_open(self):
		if self.type == 'out_invoice':
			self.check_minimum_price()
		#found a way to call the original function without override !
		super(AccountInvoice, self).action_invoice_open()
		#this means we're calling account invoice as parent of this inherited model and
		#call the action_invoice_open (true extensibility!)