import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import odoo
from odoo import fields, models, _
from odoo import SUPERUSER_ID, api
from odoo import tools
from odoo.osv import osv, expression
from odoo.tools.translate import _
from odoo.tools.float_utils import float_round as round
from odoo.exceptions import UserError, ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from odoo.tools.float_utils import float_compare
import odoo.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class back_to_back_order(models.TransientModel):
	_name = "back.to.back.order"
	_description = "Back to Back Order"

	@api.model
	def _get_picking_in(self):
		obj_data = self.env['ir.model.data']
		type_obj = self.env['stock.picking.type']	
		user_obj = self.env['res.users']
		company_id = user_obj.browse(self._context.get('uid')).company_id.id

		types = type_obj.search([['code', '=', 'incoming'], ['warehouse_id.company_id', '=', company_id]])
		if not types:
			types = type_obj.search([['code', '=', 'incoming'], ['warehouse_id', '=', False]])
			if not types:
				raise UserError(_('Make sure you have at least an incoming picking type defined'))
		return types[0]

	@api.multi
	def _pricelist_id_default(self):
		partner_obj = self.env['res.partner'] 
		pricelist_id_data = partner_obj.browse(self.env.context.get('partner_id', False)).property_purchase_currency_id.id
		return pricelist_id_data

	@api.model
	def _location_id_default(self):		
		user_obj = self.env['res.users']
		location_id_data = user_obj.browse(self._context.get('uid')).company_id.partner_id.property_stock_customer.id
		return location_id_data

	partner_id = fields.Many2one('res.partner', string='Supplier', required=True)
	date_order = fields.Datetime(string='Date Order', required=True, default=fields.Datetime.now)
	line_ids = fields.One2many('back.to.back.order.line', 'back_order_id', string='Order Lines for the Wizard', required=True,)
	location_id = fields.Many2one('stock.location', string='Destination', required=True, domain=[('usage','<>','view')], default=_location_id_default)
	picking_type_id = fields.Many2one('stock.picking.type', string="Deliver To", help="This will determine picking type of incoming shipment", required=True,
		default=_get_picking_in)
	pricelist_id = fields.Many2one('product.pricelist', string="Pricelist", required=False, states={'confirmed':[('readonly',True)], 
	'approved':[('readonly', True)], 'done':[('readonly', True)]}, help="The pricelist sets the currenct used for this purchase order. It also computes the supplier price for the selected products/quantities.",
		default= _pricelist_id_default ) 

	@api.model
	def default_get(self, fields):
		context = dict(self._context or {})
		res = super(back_to_back_order, self).default_get(fields)
		order = self.env['sale.order'].browse(self._context.get('active_ids'))
		items = []
		for line in order.order_line:
			item = 0, 0, {
				'product_id': line.product_id.id,
				'qty': line.product_uom_qty,
				'price': line.price_unit,
				'subtotal':line.price_subtotal
			}
			if line.product_id:
				items.append(item)
		res.update(line_ids=items)
		return res

	@api.multi
	def wkf_confirm_order(self):
		vals = {}
		purchase_obj = self.env['purchase.order']
		purchase_line_obj = self.env['purchase.order.line']
		product_uom = self.env['product.uom']
		product_product = self.env['product.product']
		res_partner = self.env['res.partner']
		todo = []
		supplierinfo = False
		for po in self:
			vals = {
			'partner_id': po.partner_id.id,
			'date_order': po.date_order,
			'picking_type_id': po.picking_type_id.id,
			'create_uid': self._context.get('uid')
			}
			purchase_id = purchase_obj.create(vals)

			context_partner = self._context.copy()
			if po.partner_id.id:
				lang = res_partner.browse(po.partner_id.id).lang
				context_partner.update({'lang': lang, 'partner_id': po.partner_id.id})

			for line in po.line_ids:
				if line.qty <= 0:
					continue
				else:
					product = product_product.with_context(context_partner).browse(line.product_id.id)
					dummy, name = product_product.with_context(context_partner).browse(line.product_id.id).name_get()[0]
					if product.description_purchase:
						name += '\n' + product.description_purchase
					precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
					for supplier in product.seller_ids:
						if po.partner_id.id and (supplier.name.id == po.partner_id.id):
							supplierinfo = supplier
							if supplierinfo.product_uom.id != line.product_uom.id:
								raise UserError(_('The selected supplier only sells this product by %s') 
								% (supplierinfo.product_uom.name))
							min_qty = supplierinfo.min_qty				
							if float_compare(min_qty, line.qty, precision_digits=precision) == 1: #If the supplier quantity is greater than entered from user, set minimal.
								if line.qty:
									raise UserError(_('The selected supplier has a minimal quanitity set to %s %s, you should not purchase less.')
									 % (supplierinfo.min_qty, supplierinfo.product_uom.name))
								line.qty = min_qty
								return {'warning': warning_mess}
					dt = purchase_line_obj._get_date_planned(supplierinfo).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
					values = {
						'product_id': line.product_id.id,
						'name': name,
						'date_planned': dt,
						'product_qty': line.qty,
						'price_unit': line.price,
						'price_subtotal': line.subtotal,
						'order_id': purchase_id.id,
						'sale_order_id': self._context['active_id'],
						'product_uom': line.product_id.uom_po_id.id,					
					}
		 			line_id = self.env['purchase.order.line'].with_context(self._context).create(values)

class back_to_back_order_line(models.TransientModel):
	_name = "back.to.back.order.line"
	_description = "Back to Back Order"

	@api.multi
	def _amount_line(self):
		res = {}
		cur_obj = self.env['res.currency']
		tax_obj = self.env['account.tax']
		for line in self.browse():
			taxes = tax_obj.compute_all(line.taxes_id, line.price, line.qty, line.product_id, line.back_order_id.partner_id)
			cur = line.back_order_id.pricelist_id.currency_id
			res[line.id] = cur_obj.round(cur, taxes['total'])
		return res

	@api.model
	def _get_uom_id(self):
		try:
			proxy = self.env['ir.model.data']
			result = proxy.get_object_reference('product', 'product_uom_unit')
			return result[1]
		except Exception, ex:
			return False

	@api.onchange('product_id')
	def onchange_product_id(self):
		result = {}
		if not self.product_id:
			return result

		unit_cost = self.product_id.standard_price
		self.price = unit_cost

		return result

	@api.onchange('qty')
	def onchange_qty(self):
		result = {}
		if not self.product_id:
			return result

		total = self.price * self.qty
		self.subtotal = total

		return result

	product_id = fields.Many2one('product.product', string="Product")
	back_order_id = fields.Many2one('back.to.back.order', string="Back Order")
	qty = fields.Float(string="Quantity")
	price = fields.Float(string="Unit Price")
	subtotal = fields.Float(string="Subtotal", compute='_amount_line')
	taxes_id = fields.Many2many('account.tax', 'purchase_order_taxes', 'ord_id', 'tax_id', string="Taxes")
	product_uom = fields.Many2one('product.uom', string="Product Unit of Measure", default=_get_uom_id)
