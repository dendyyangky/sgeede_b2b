from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	unit_cost = fields.Float(string="Unit Cost")

	@api.multi
	@api.onchange('product_id')
	def get_cost(self):
		print "get_cost is called"
		if not self.product_id:
			return False

		vals = {}

		vals['unit_cost'] = self.product_id.standard_price
		self.update(vals)

		return

#overriding create method to include cost to the record
	@api.model
	def create(self, values):
		onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id', 'unit_cost']
		if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
			line = self.new(values)
			line.product_id_change()
			line.get_cost()
			for field in onchange_fields:
				if field not in values:
					values[field] = line._fields[field].convert_to_write(line[field], line)
		print "values in create"
		print values
		line = super(SaleOrderLine, self).create(values)
		if line.state == 'sale':
			line.action_procurement_create()

		return line