from openerp import netsvc
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import datetime
from openerp.osv import osv
import time

class wizard_stock_internal_transfer(models.TransientModel):
	_name = 'wizard.stock.internal.transfer'

	transfer_id = fields.Many2one('stock.internal.transfer', 'Transfer')
	item_ids = fields.One2many('stock.internal.transfer.items', 'transfer_id', 'Items')

	def default_get(self, cr, uid, fields, context=None):
		if context is None: context = {}
		res = super(wizard_stock_internal_transfer, self).default_get(cr, uid, fields, context=context)
		transfer_ids = context.get('active_ids', [])
		active_model = context.get('active_model')

		if not transfer_ids: #or len(transfer_ids) != 1:
			# Partial Picking Processing may only be done for one picking at a time
			return res
		assert active_model in ('stock.internal.transfer'), 'Bad context propagation'
		transfer_id = transfer_ids
		transfers = self.pool.get('stock.internal.transfer').browse(cr, uid, transfer_id, context=context)

		company_id = self.pool.get('res.users').browse(cr, uid, uid).company_id.id
		company = self.pool.get('res.company').browse(cr, uid, company_id)

		items = []

		if not company.transit_location_id:
			raise osv.except_osv(_('Error!'), _('Please setup your stock transit location in Setting - Internal Transfer Configuration'))

		if transfers.state == 'draft':
			source_location_id = transfers.source_warehouse_id.lot_stock_id.id
			dest_location_id = company.transit_location_id.id
		elif transfers.state == 'send':
			source_location_id = company.transit_location_id.id
			dest_location_id = transfers.dest_warehouse_id.lot_stock_id.id

		for transfer in transfers.line_ids:
			item = {
				'product_id': transfer.product_id.id,
				'product_uom_id': transfer.product_uom_id.id,
				'product_qty': transfer.product_qty,
				'source_location_id': source_location_id,
				'dest_location_id': dest_location_id,
			}
			if transfer.product_id:
				items.append(item)

		res.update(item_ids=items)
		return res

	def button_confirm(self, cr, uid, ids, context):
		for tf in self.browse(cr, uid, ids):
			if 'active_ids' in context:
				transfer = self.pool.get('stock.internal.transfer').browse(cr, uid, context.get('active_ids'))
				company_id = self.pool.get('res.users').browse(cr, uid, uid).company_id.id
				company = self.pool.get('res.company').browse(cr, uid, company_id)
				if transfer.state == 'draft':
					backorders = []
					user_list = []
					user_ids = transfer.source_warehouse_id.user_ids
					if user_ids :
						for user in user_ids :
							user_list.append(user.id)

					if uid not in user_list:
						raise osv.except_osv(_('Warning !'), _('You are not authorized to send or receive products !'))

					for line in tf.item_ids:
						for trans in transfer.line_ids:
							if line.product_id.id == trans.product_id.id:
								if line.product_qty > trans.product_qty:
									raise osv.except_osv(_('Error!'), _('You have exceed the available product quantity'))
								elif line.product_qty < trans.product_qty:
									backorder = {
									'product_id' : line.product_id.id,
									'product_qty': trans.product_qty - line.product_qty,
									'product_uom_id' : line.product_uom_id.id,
									'state' : 'draft',
									}
									backorders.append(backorder)

									self.pool.get('stock.internal.transfer.line').write(cr, uid, trans.id, {
										'product_qty': line.product_qty
										})

					if backorders:
						create_id = self.pool.get('stock.internal.transfer').create(cr, uid, {
							'date' : time.strftime('%Y-%m-%d %H:%M:%S'),
							'source_location_id': transfer.source_location_id.id,
							'dest_location_id': transfer.dest_location_id.id,
							'backorder_id': context.get('active_ids')[0],
							'state': 'draft',
							})
						for backorder in backorders:
							backorder['transfer_id'] = create_id
							self.pool.get('stock.internal.transfer.line').create(cr, uid, backorder)

					type_obj = self.pool.get('stock.picking.type')
					type_ids = type_obj.search(cr, uid, [('default_location_src_id', '=', transfer.source_warehouse_id.lot_stock_id.id),
						('code', '=', 'outgoing')])

					if type_ids:
						types = type_obj.browse(cr, uid, type_ids[0])

						picking_obj = self.pool.get('stock.picking')
						picking_id = picking_obj.create(cr, uid, {
							'picking_type_id': types.id,
							'transfer_id': context.get('active_ids'),
							'location_id': transfer.source_warehouse_id.lot_stock_id.id,
							'location_dest_id': company.transit_location_id.id,
							})
					else:
						raise osv.except_osv(_('Error!'), _('Unable to find source location in Stock Picking'))

					move_obj = self.pool.get('stock.move')

					for line in tf.item_ids:

						move_obj.create(cr, uid, {
							'name' : 'Stock Internal Transfer',
							'product_id' : line.product_id.id,
							'product_uom' : line.product_uom_id.id,
							'product_uom_qty' : line.product_qty,
							'location_id' : line.source_location_id.id,
							'location_dest_id' : line.dest_location_id.id,
							'picking_id' : picking_id,
							})

					immediate_transfer_obj = self.pool.get('stock.immediate.transfer')
					picking_obj = self.pool.get('stock.picking')
					picking_obj.action_confirm(cr, uid, picking_id)
					picking_obj.action_assign(cr, uid, picking_id)
					picking_obj.do_new_transfer(cr, uid, picking_id)
					picking_obj.do_transfer(cr, uid, picking_id)
					picking_obj.do_internal_transfer_details(cr, uid, picking_id)

					wkf_service = netsvc.LocalService('workflow')
					wkf_service.trg_validate(uid, 'stock.internal.transfer', context.get('active_ids'), 'action_send', cr)

				elif transfer.state == 'send':
					backorders = []
					user_list = []
					user_ids = transfer.dest_warehouse_id.user_ids
					if user_ids :
						for user in user_ids :
							user_list.append(user.id)

					if uid not in user_list:
						raise osv.except_osv(_('Warning!'), _('You are not authorized to send or receive products !'))

					for line in tf.item_ids:
						for trans in transfer.line_ids:
							if line.product_id.id == trans.product_id.id:
								if line.product_qty > trans.product_qty:
									raise osv.except_osv(_('Error!'), _('You have exceed the available product quantity'))
								elif line.product_qty < trans.product_qty:
									backorder = {
										'product_id' : line.product_id.id,
										'product_qty': trans.product_qty - line.product_qty,
										'product_uom_id' : line.product_uom_id.id,
										'state': 'draft',
									}
									backorders.append(barckorder)
					if backorders:
						create_id = self.pool.get('stock.internal.transfer').create(cr, uid, {
								'date' : time.strftime('%Y-%m-%d %H:%M:%S'),
								'source_location_id' : transfer.source_location_id,
								'dest_location_id' : transfer.dest_location_id.id,
								'backorder_id' : context.get('active_ids')[0],
								'state' : 'send',
							})
						for backorder in backorders:
							backorder['transfer_id'] = create_id
							self.pool.get('stock.internal.transfer', create_id, 'action_send', cr)
						wkf_service.trg_validate(uid, 'stock.internal.transfer', create_id, 'action_send', cr)

					type_obj = self.pool.get('stock.picking.type')
					type_ids = type_obj.search(cr, uid, [('default_location_dest_id', '=', transfer.dest_warehouse_id.lot_stock_id.id),
						('code', '=', 'incoming')])

					if type_ids:
						types = type_obj.browse(cr, uid, type_ids[0])

						picking_obj = self.pool.get('stock.picking')
						picking_id = picking_obj.create(cr, uid, {
							'picking_type_id' : types.id,
							'transfer_id' : context.get('active_ids'),
							'location_id': company.transit_location_id.id,
							'location_dest_id': transfer.dest_warehouse_id.lot_stock_id.id, 
							})
					else:
						raise osv.except_osv(_('Error!'), _('Unable to find destination location in Stock Picking.'))

					move_obj = self.pool.get('stock.move')

					for line in tf.item_ids:
						move_obj.create(cr, uid, {
							'name': 'Stock Internal Transfer',
							'product_id' : line.product_id.id,
							'product_uom' : line.product_uom_id.id,
							'product_uom_qty' : line.product_qty,
							'location_id' : line.source_location_id.id,
							'location_dest_id' : line.dest_location_id.id,
							'picking_id' : picking_id,
							})

					picking_obj = self.pool.get('stock.picking')
					picking_obj.action_confirm(cr, uid, picking_id)
					picking_obj.action_assign(cr, uid, picking_id)
					picking_obj.do_new_transfer(cr, uid, picking_id)
					picking_obj.do_transfer(cr, uid, picking_id)
					picking_obj.do_internal_transfer_details(cr, uid, picking_id)
#do_internal_transfer_details is not used ? 					

					wkf_service = netsvc.LocalService('workflow')
					wkf_service.trg_validate(uid, 'stock.internal.transfer', context.get('active_ids'), 'action_receive', cr)

		return True

	@api.multi
	def wizard_view(self):
		view = self.env.ref('sgeede_internal_transfer.wizard_stock_internal_transfer_view')
		return {
			'name': _('Enter Transfer Details'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'wizard.stock.internal.transfer',
			'views': [(view.id, 'form')],
			'view_id': view.id,
			'target': 'new',
			'res_id': self.ids[0],
			'context': self.env.context,
		}

class stock_internal_transfer_item(models.TransientModel):
	_name = 'stock.internal.transfer.items'

	transfer_id = fields.Many2one('wizard.stock.internal.transfer', 'Transfer')
	product_id = fields.Many2one('product.product', 'Product')
	product_qty = fields.Float('Quantity')
	product_uom_id = fields.Many2one('product.uom', 'Unit of Measure')
	source_location_id = fields.Many2one('stock.location', 'Source Location')
	transit_location_id = fields.Many2one('stock.location', 'Transit Location')
	dest_location_id = fields.Many2one('stock.location', 'Destination Location')

	def product_id_change(self, cr, uids, product_id, context=None):
		result = {}
		if not product_id:
			return{'value': {
			'product_uom_id': False,
			}}

		product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)

		product_uom_id = product.uom_id and product.uom_id.id or False

		result['value'] = {'product_uom_id': product_uom_id}
		return result