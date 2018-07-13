from odoo import api, fields, models, tools, _

class ProductTemplate(models.Model):
	_inherit = "product.template"

	minimum_price = fields.Float(string="Minimum Price", help="The lowest price allowed for this product to be sold", default=0.0)