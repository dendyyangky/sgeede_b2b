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

class stock_picking(osv.osv):
	_inherit = "stock.picking"

	@api.cr_uid_ids_context
	def do_internal_transfer_details(self, cr, uid, picking, context=None):
		if not context:
			context = {}

		picking = [picking]

		context.update({
			'active_model': self._name,
			'active_ids': picking,
			'active_id': len(picking) and picking[0] or False
		})

		created_id = self.pool['stock.transfer_details'].create(cr, uid, {'picking_id': len(picking) and picking[0] or False}, context)
		self.pool['stock.transfer_details'].do_detailed_transfer(cr, uid, created_id)

		return True

	_columns = {
		'transfer_id'	: fields.many2one('stock.internal.transfer', 'Transfer'),
	}

class stock_move(osv.osv):
	_inherit = "stock.move"

	_columns = {
		'analytic_account_id' : fields.many2one('account.analytic.account','Analytic Account'),
	}

class stock_move(osv.osv):
	_inherit = "stock.warehouse"

	_columns = {
		'user_ids' : fields.many2many('res.users','company_user_rel','company_id','user_id','Owner user'),
	}