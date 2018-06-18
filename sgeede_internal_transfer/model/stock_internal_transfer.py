from datetime import date, datetime
from dateutil import relativedelta
import json
import time

from openerp.osv import fields, osv
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp import SUPERUSER_ID, api
import openerp.addons.decimal_precision as dp
from openerp.addons.procurement import procurement
import logging

_logger = logging.getLogger(__name__)

class stock_internal_transfer(osv.osv):
	_name = 'stock.internal.transfer'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	@api.multi
	def action_cancel(self):
		self.write({'state' : 'cancel'})
		return True

	def action_draft(self, cr, uid, ids, context):
		self.write(cr, uid, ids, {
			'state' : 'draft'
			})
		return True

	def action_send(self, cr, uid, ids, context):
		self.write(cr, uid, ids, {
			'state' : 'send'
			})
		return True

	def action_receive(self, cr, uid, ids, context):
		self.write(cr, uid, ids, {
			'state' : 'done'
			})
		return True
		
	def do_enter_wizard(self, cr, uid, ids, context):
		if not context:
			context = {}

		context.update({
			'active_model': self._name,
			'active_ids': ids,
			'active_ids': len(ids) and ids[0] or False
			})

		created_id = self.pool['wizard.stock.internal.transfer'].create(cr, uid, {'transfer_id': len(ids) and ids[0] or False}, context)
		return self.pool['wizard.stock.internal.transfer'].wizard_view(cr, uid, created_id, context)


	_columns = {
		'name' : fields.char('Reference', track_visibility='onchange'),
		'date' : fields.datetime('Data', track_visiblity='onchange'),
		'source_warehouse_id' : fields.many2one('stock.warehouse', 'Source Warehouse', track_visibility='onchange'),
		'dest_warehouse_id' : fields.many2one('stock.warehouse', 'Destination Warehouse', track_visibility ='onchange'),
		'state': fields.selection([('cancel', 'Cancel'), ('draft', 'Draft'), ('send', 'Send'), ('done', 'Done')], 'Status', 
			track_visibility='onchange'),
		'line_ids' : fields.one2many('stock.internal.transfer.line', 'transfer_id', 'Stock Internal Transfer Line'),
		'picking_ids': fields.one2many('stock.picking', 'transfer_id', 'Picking'),
		'backorder_id' : fields.many2one('stock.internal.transfer', 'Backorder'),
	}

	_defaults = {
		'name': lambda self, cr, uid, c: self.pool.get('ir.sequence').next_by_code(cr, uid, 'stock.internal.transfer') or '',
		'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
		'state': lambda *a: 'draft',
	}

class stock_internal_transfer_line(osv.osv):
	_name = 'stock.internal.transfer.line'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	def product_id_change(self, cr ,uid, ids, product_id, context=None):
		result = {}
		if not product_id:
			return {'value': {
			'product_uom_id': False,
			}}

		product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)

		product_uom_id = product.uom_id and product.uom_id.id or False

		result['value'] = {'product_uom_id': product_uom_id}
		return result

	_columns = {
		'name' : fields.char('Reference', track_visiblity='onchange'),
		'product_id' : fields.many2one('product.product', 'Product', track_visibility='onchange'),
		'product_qty' : fields.float('Quantity', track_visibility='onchange'),
		'product_uom_id' : fields.many2one('product.uom', 'Unit of Measure', track_visibility='onchange'),
		'state' : fields.selection([('cancel', 'Cancel'), ('draft', 'Draft'), ('send', 'Send'), ('done', 'Done')],
			'Status', track_visibility='onchange'),
		'transfer_id' : fields.many2one('stock.internal.transfer', 'Transfer', track_visibility='onchange'),
	}

	_defaults = {
		'state' : lambda *a: 'draft',
		'product_qty' : lambda *a: 1,
	}