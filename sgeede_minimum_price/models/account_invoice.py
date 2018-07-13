from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class account_invoice(models.Model):
	_inherit = "account.invoice"

#if we can modify/override workflow, this will be much more cleaner
# search action_date_assign() in /account/account_invoice_workflow.xml
	@api.multi
	def check_min_price(self):
		for o in self:
			if not o.invoice_line:
				return False
			for line in o.invoice_line:
				if line.product_id and (line.price_unit < line.product_id.product_tmpl_id.minimum_price):
					raise except_orm(_('Error'), _("Price is lower than the minimum product price! \n Please recheck %s") % (line.product_id.name))
		return True