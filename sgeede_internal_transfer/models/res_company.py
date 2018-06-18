from datetime import date, datetime
from dateutil import relativedelta
import json
import time

from odoo import fields, models
from odoo.tools import float_compare
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo import SUPERUSER_ID, api
import odoo.addons.decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

class res_company(models.Model):
	_inherit = "res.company"

	transit_location_id = fields.Many2one('stock.location', 'Transit Location')