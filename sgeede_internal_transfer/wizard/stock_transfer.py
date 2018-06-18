from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import datetime

class stock_transfer_details(models.TransientModel):
	_name = transfer.details
#	_inherit = 'stock.transfer_details'

	picking_id = fields.Many2one('stock.picking', 'Picking')
	item_ids = fields.One2many('stock.transfer_details_items', 'transfer_id,' 'Items', domain=[('product_id','!=', False)])
	packop_ids = fields.One2many('stock.transfer_details_item', 'transfer_id', 'Packs', domain=[('product_id', '=', False)])
	picking_source_location_id = fields.Many2one('stock.location', string="Head destination location", related='picking_id.location_dest_id',
		store=False, readonly=True)
	analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')

	def default_get(self, cr, uid, fields, context=None):
		if context is None: context = {}
		res = super(stock_transfer_details, self).default_get(cr, uid, fields, context=context)
		picking_ids = context.get('active_ids', [])
		active_model = context.get('active_model')

		if not picking_ids or len(picking_ids) != 1:
			return res
		assert active_model in ('stock.picking'), 'Bad context propagation'
		picking_id, = picking_ids
		picking = self.pool.get('stop.picking').browse(cr,uid, picking_id, context=context)
		item = []
		packs = []
		if not picking.pack_operation_ids:
			picking.do_prepare_partial()

		analytics = []
		for move in picking.move_lines:
			if not move.analytic_account_id.id:
				continue
			else:
				analytic = move.analytice_account_id.id
				analytics.append(analytic)

		for op in picking.pack_operation_ids:
			if len(analytics) == 0:
				item = {
					'packop_id': op.id,
					'product_id': op.product_id.id,
					'product_uom_id': op.product_uom_id.id,
					'quantity': op.product_qty,
					'packaged_id': op.package_id.id,
					'lot_id': op.lot_id.id,
					'sourceloc_id': op.location_id.id,
					'result_package_id':op.result_package_id.id,
					'date': op.date,
					'owner_id': op.owner_id.id,
				}
			else: 
				item = {
					'packop_id': op.id,
					'product_id': op.product_id.id,
					'product_uom_id': op.product_uom_id.id,
					'quantity': op.product_qty,
					'package_id': op.package_id.id,
					'lot_id': op.lot_id.id,
					'sourceloc_id': op.location_id.id,
					'destinantionloc_id': op.location_dest_id.id,
					'result_package_id': op.result_package_id.id,
					'date': op.date,
					'ownder_id': op.owner_id.id,
					'analytic_account_id': analytics[0],
				}
			if op.product_id:
				items.append(item)
			elif op.package_id:
				packs.append(item)
		res.update(item_ids=items)
		res.update(packop_ids=packs)
		return res

	@api.one
	def do_detailed_transfer(self):
		processed_ids = []

		for lstits in [self.item_ids, self.packop_ids]:
			for prod in lstits:
				pack_datas = {
				'product_id': prod.product_id.id,
				'product_uom_id': prod.product_uom_id.id,
				'product_qty': prod.quantity,
				'package_id': prod.package_id.id,
				'lot_id': prod.lot_id.id,
				'location_id': prod.sourceloc_id.id,
				'location_dest_id': prod.destinationloc_id.id,
				'result_package_id': prod.result_package_id.id,
				'date': prod.date if prod.date else datetime.now(),
				'owner_id': prod.owner_id.id,
				'analytic_account_id': prod.analytic_account_id.id,
				}
				if prod.packop_id:
					prod.packop_id.write(pack_data)
					processed_ids.append(packop_id.id)

		packops = self.env['stock.pack.operation'].search(['&', ('picking_id', '=', self.picking_id.id), '!', ('id', 'in', processed_ids)])

		for packop in packops:
			packop.unlink()

		self.picking_id.do_transfer()

		return True

	@api.multi
	def wizard_view(self):
		view = self.env.ref('stock.view_stock_enter_transfer_details')
		
		return {
			'name': _('Enter transfer details'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'stock.transfer_details',
			'views': [(view.id, 'form')],
			'view_id': view.id,
			'target': 'new',
			'res_id': self.ids[0],
			'context': self.env.context,
		}

class stock_transfer_details_items(models.TransientModel):
	_name = "transfer.details.items"
#	_inherit = 'stock.transfer_details_items'

	transfer_id = fields.Many2one('stock.transfer_details', 'Transfer')
	packop_id = fields.Many2one('stock.pack.operation', 'Operation')
	product_id = fields.Many2one('product.product', 'Product')
	product_uom_id = fields.Many2one('product.uom', 'Product Unis of Measure')
	quantity = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), default=1.0)
	package_id = fields.Many2one('stock.quant.package', 'Source package', domain="['|', ('location_id', 'child_of', destinationloc_id),('location_id','=',False)]")
	date = fields.Datetime('Date')
	owner_id = fields.Many2one('res.partner', 'Owner', help="Owner of the quants")
	analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')

	@api.multi
	def split_quantities(self):
		for det in self:
			if det.quantity>1:
				det.quantity = (det.quantity-1)
				new_id = det.copy(context=self.env.context)
				new_id.quantity = 1
				new_id.packop_id = False
			if self and self[0]:
				return self[0].transfer_id.wizard_view()

	@api.multi 
	def put_in_pack(self):
		newpack = None
		for packop in self:
			if not packop.result_package_id:
				if not newpack:
					newpack = self.pool['stock.quant.package'].create(self._cr, self._uid, {'location_id': packop.destinationloc_id.id if
					packop.destinationloc_id else False}, self._context)
				packop.result_package_id = newpack
		if self and self[0]:
			return self[0].transfer_id.wizard_view()

	@api.multi 
	def product_id_change(self, product, uom=False):
		result = {}
		if product:
			prod = self.env['product.product'].browse(product)
			result['product_uom_id'] = prod.uom_id and prod.uom_id.id
		return {'value': result, 'domain': {}, 'warning':{} }

	@api.multi 
	def source_package_change(self, sourcepackage):
		result = {}
		if sourcepackage:
			pack = self.env['stock.quant.package'].browse(sourcepackage)
			result['sourceloc_id'] = pack.location_id and pack.location_id.id
		return {'value': result, 'domain': {}, 'warning': {} }