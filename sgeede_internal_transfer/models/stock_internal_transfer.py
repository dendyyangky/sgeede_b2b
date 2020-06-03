# -*- coding: utf-8 -*-
import json
import time
import logging
import odoo.addons.decimal_precision as dp
from datetime import date, datetime
from dateutil import relativedelta
from odoo import fields, models
from odoo.tools import float_compare
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo import SUPERUSER_ID, api
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class stock_internal_transfer(models.Model):
    _name = 'stock.internal.transfer'
    _inherit = 'mail.thread'

    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True

    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    def action_send(self):
        self.write({'state': 'send'})
        return True

    def action_receive(self):
        self.write({'state': 'done'})
        return True

    def do_enter_wizard(self):
        ctx = dict(self._context)

        ctx.update({
            'active_model': self._name,
            'active_ids': self._ids,
            'active_id': len(self._ids) and self._ids[0] or False
            })

        created_id = self.env['wizard.stock.internal.transfer'].with_context(ctx).create({'transfer_id': len(self._ids) and self._ids or False}).id
        return self.env['wizard.stock.internal.transfer'].with_context(ctx).wizard_view(created_id)

    name = fields.Char(string= 'Reference', track_visibility="onchange", default= lambda self: self.env['ir.sequence'].next_by_code('stock.internal.transfer') or '')
    date = fields.Datetime(string= 'Date', track_visibility="onchange", default= lambda self: time.strftime('%Y-%m-%d %H:%M:%S'))
    source_warehouse_id = fields.Many2one('stock.warehouse', string="Source Warehouse", track_visibility="onchange")
    dest_warehouse_id = fields.Many2one('stock.warehouse', string="Destination Warehouse", track_visibility="onchange")
    state = fields.Selection([('cancel', 'Cancel'), ('draft', 'Draft'), ('send', 'Send'), ('done', 'Done')], string="Status", track_visibility="onchange", default="draft")
    line_ids = fields.One2many('stock.internal.transfer.line', 'transfer_id', string="Stock Internal Transfer Line")
    picking_ids = fields.One2many('stock.picking', 'transfer_id', string="Picking")
    backorder_id = fields.Many2one('stock.internal.transfer', 'Backorder')

class stock_internal_transfer(models.Model):
    _name = 'stock.internal.transfer.line'
    _inherit = 'mail.thread'

    @api.onchange('product_id')
    def product_id_change(self):
        result = {}
        if not self.product_id: {
            'product_uom_id': False,
        }
        product = self.env['product.product'].browse(self.product_id.id)
        product_uom_id = product.uom_id and product.uom_id.id or False
        result['value'] = {'product_uom_id': product_uom_id}
        return result

    name = fields.Char(string="Reference", track_visibility='onchange')
    product_id = fields.Many2one('product.product', string="Product", track_visibility="onchange")
    product_qty = fields.Float(string="Quantity", track_visibility="onchange", default=1)
    product_uom_id = fields.Many2one('product.uom', string="Unit of Measure", track_visibility='onchange')
    state = fields.Selection([('cancel', 'Cancel'), ('draft', 'Draft'), ('send', 'Send'), ('done', 'Done')],
        string="Status", track_visibility='onchange', default="draft")
    transfer_id = fields.Many2one('stock.internal.transfer', string="Transfer", track_visibility="onchange")