from openerp.osv import osv, fields, expression

class product_template(osv.osv):
	_inherit = "product.template"

	_columns = {
	'minimum_price' : fields.float('Minimum Price', help="The lowest price allowed for this product to be sold"),
	}

	_defaults = {
	'minimum_price' : 0.0,
	}