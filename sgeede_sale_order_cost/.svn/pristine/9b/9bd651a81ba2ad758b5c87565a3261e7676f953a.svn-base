from openerp import api, fields, models, _

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	unit_cost = fields.Float(string="Unit Cost")
	#setting default on unit_cost prevents it from getting saved into record
	
	@api.multi
	@api.onchange('product_id')
	def get_cost(self):
		print "get cost is called========="
		if not self.product_id:
			return False

		vals = {}

		vals['unit_cost'] = self.product_id.standard_price
		self.update(vals)
		return

#override the create method to include cost
	@api.model
	def create(self, values):
		onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id', 'unit_cost']
		if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
			line = self.new(values)
			line.product_id_change()
			line.get_cost()
			print "values after product_id_change()"
			print values
			for field in onchange_fields:
				if field not in values:
					values[field] = line._fields[field].convert_to_write(line[field])
		line = super(SaleOrderLine, self).create(values)
		if line.state == 'sale':
			if (not line.order_id.project_id and (line.product_id.track_service in self._get_analytic_track_service() or line.product_id.invoice_policy in self._get_analytic_invoice_policy())):
				line.order_id._create_analytic_account()
			line._action_procurement_create()

		return line

# #overriding onchange_product_id to include cost
	# @api.multi
	# @api.onchange('product_id')
	# def product_id_change(self):
	# 	if not self.product_id:
	# 		return {'domain': {'product_uom': []}}

	# 	vals = {}
	# 	domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
	# 	if not self.product_uom or (self.product_id.uom_id.category_id.id != self.product_uom.category_id.id):
	# 		vals['product_uom'] = self.product_id.uom_id

	# 	product = self.product_id.with_context(
	# 		lang = self.order_id.partner_id.lang,
	# 		partner = self.order_id.partner_id.id,
	# 		quantity = self.product_uom_qty,
	# 		date = self.order_id.date_order,
	# 		pricelist = self.order_id.pricelist_id.id,
	# 		uom = self.product_uom.id
	# 		)

	# 	name = product.name_get()[0][1]
	# 	if product.description_sale:
	# 		name += '\n' + product.description_sale
	# 	vals['name'] = name

	# 	if product.standard_price:
	# 		cost = product.standard_price
	# 	vals['unit_cost'] = cost

	# 	self._compute_tax_id()

	# 	if self.order_id.pricelist_id and self.order_id.partner_id:
	# 		vals['price_unit'] = self.env['account.tax']._fix_tax_included_price(product.price, product.taxes_id, self.tax_id)
	# 	self.update(vals)

	# 	return {'domain': domain}


				