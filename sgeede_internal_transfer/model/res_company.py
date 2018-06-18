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

class res_company(osv.osv):
	_inherit = "res.company"

	_columns = {
		'transit_location_id' : fields.many2one('stock.location', 'Transit Location'),
	}