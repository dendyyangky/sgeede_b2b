from odoo import api, fields, models, _

class sale_order_line(models.Model):
	_inherit = 'sale.order.line'

	unit_cost = fields.Float(string="Unit Cost")

	@api.multi
	@api.onchange('product_id')
	def get_cost(self):
		if not self.product_id:
			return False

		val = {}

		val['unit_cost'] = self.product_id.standard_price
		self.update(val)

		return

#overriding prepare_add_missing_field to include cost 
	@api.model
	def _prepare_add_missing_fields(self, values):
		print ("values needs to be checked===========")
		print (values)
		res = {}
		onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id', 'unit_cost']
		if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
			line = self.new(values)
			line.product_id_change()
			line.get_cost()
			for field in onchange_fields:
				if field not in values:
					res[field] = line._fields[field].convert_to_write(line[field], line)
		return res

