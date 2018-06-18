from odoo import api, fields, models, _

class sgeede_config_settings(models.TransientModel):
	_name = 'sgeede.config.settings'
	_inherit = 'res.config.settings'

	company_id = fields.Many2one('res.company', string="Company", required= True,
		default= lambda self: self.env['res.users'].browse(self._uid).company_id.id)
	transit_location_id = fields.Many2one(string="Transit Location", related="company_id.transit_location_id", relation="stock.location")
# not needed ?
	@api.onchange('company_id')
	@api.multi
	def on_change_company_id(self):
		print ("called")
		#website_data = self.read(self.company_id, [])
		# ^ gives read error

  #       for fname in fields:
  #           field = self._fields[fname]
  #           if field.type == 'many2one':
  #               values[fname] = self[fname].id
  #           elif field.type == 'one2many':
  #               raise AssertionError(_('One2Many fields cannot be synchronized as part of `commercial_fields` or `address fields`'))
  #           elif field.type == 'many2many':
  #               values[fname] = [(6, 0, self[fname].ids)]
  #           else:
  #               values[fname] = self[fname]
  #       return values
		# values = {}
		# for fname, v in website_data.items():
		# 	if fname in self._columns:
		# 		values[fname] = v[0] if v and self._columns[fname]._type == 'many2one' else v

	@api.onchange('transit_location_id')
	def onchange_transit_location_id(self):

		values = {
			'transit_location_id' : self.transit_location_id
		}
		return {'value': values}

	@api.model
	def create(self, vals):
		config_id = super(sgeede_config_settings, self).create(vals)
		self.write(vals)
		return config_id