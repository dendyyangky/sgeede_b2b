##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools.float_utils import float_compare
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class back_to_back_order(osv.osv_memory):
    _name = "back.to.back.order"
    _description = "Back to Back Order"
    
    
    def _get_picking_in(self, cr, uid, context=None):
        obj_data = self.pool.get('ir.model.data')
        type_obj = self.pool.get('stock.picking.type')
        user_obj = self.pool.get('res.users')
        company_id = user_obj.browse(cr, uid, uid, context=context).company_id.id
        types = type_obj.search(cr, uid, [('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)], context=context)
        if not types:
            types = type_obj.search(cr, uid, [('code', '=', 'incoming'), ('warehouse_id', '=', False)], context=context)
            if not types:
                raise osv.except_osv(_('Error!'), _("Make sure you have at least an incoming picking type defined"))
        return types[0]
    
    
#    def _get_pricelist(self, cr, uid, context=None):
#        ctx = dict(context or {})
#        order = self.pool.get('sale.order').browse(cr, uid, ctx['active_id'], context=context)
#        print order.partner_id.name
#        
#        partner_id = context.get('partner_id', False)
#        if partner_id:
#            pricelist_ids = self.pool.get('res.partner').browse(cr, uid, order.partner_id.id).property_product_pricelist_purchase.id
#            return pricelist_ids[0]
#        else:
#            return False
        
        
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        partner = self.pool.get('res.partner')
        if not partner_id:
            return {}
        supplier = partner.browse(cr, uid, partner_id, context=context)
        return {'value': {
            'pricelist_id': supplier.property_product_pricelist_purchase.id,
#            'fiscal_position': supplier.property_account_position and supplier.property_account_position.id or False,
#            'payment_term_id': supplier.property_supplier_payment_term.id or False,
            }}
    
    
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Supplier', required=True),
        'date_order':     fields.datetime('Date Order', required=True),
        'line_ids': fields.one2many('back.to.back.order.line','back_order_id', 'Order Lines', required=True),
        'location_id': fields.many2one('stock.location', 'Destination', required=True, domain=[('usage','<>','view')]),
        'picking_type_id': fields.many2one('stock.picking.type', 'Deliver To', help="This will determine picking type of incoming shipment", required=True),
        'pricelist_id':fields.many2one('product.pricelist', 'Pricelist', help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."),
        'currency_id': fields.many2one('res.currency','Currency', readonly=True),
        
    }
    
    _defaults = {
        'date_order': fields.datetime.now,
#        'pricelist_id': lambda self, cr, uid, context: context.get('partner_id', False) and self.pool.get('res.partner').browse(cr, uid, context['partner_id']).property_product_pricelist_purchase.id,
#        'pricelist_id': _get_pricelist,
        
        'location_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.partner_id.property_stock_customer.id,
        'currency_id': lambda self, cr, uid, context: self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id.id,
        'picking_type_id': _get_picking_in,
    }
    
    
    def onchange_pricelist(self, cr, uid, ids, pricelist_id, line_ids,partner_id, context=None):
        product_pricelist = self.pool.get('product.pricelist')
        
        if not pricelist_id or not line_ids :
            return {}
        else:
            items = [(6, 0, [])]
            for line in line_ids:
                val = line[2]
                if not val:
                    continue
                else:
                    product = self.pool.get('product.product').browse(cr, uid, int(val['product_id']), context=context)
                    date_order = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    date_order_str = datetime.strptime(date_order, DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
                    price = product_pricelist.price_get(cr, uid, [int(pricelist_id)],
                            product.id, val['qty'] or 1.0, int(partner_id) or False, {'uom': product.uom_po_id.id, 'date': date_order_str})[int(pricelist_id)]
                    if price is False:
                        price = product.standard_price
                    item = 0,0,{'product_id': val['product_id'],
                            'qty': val['qty'],
                            'price': price or 0.0,
                            'subtotal': price * val['qty']
                            }
                    if val['product_id']:
                        items.append(item)
                    
            return {'value': {'currency_id': self.pool.get('product.pricelist').browse(cr, uid, pricelist_id, context=context).currency_id.id,
                      'line_ids' : items}}

    
    def default_get(self, cr, uid, fields, context=None):
        product_pricelist = self.pool.get('product.pricelist')
        if context is None:
            context = {}
        res = super(back_to_back_order, self).default_get(cr, uid, fields, context=context)
        order = self.pool.get('sale.order').browse(cr, uid, context['active_id'], context=context)
        items = []
        date_order = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for line in order.order_line:
            
            # - determine price_unit and taxes_id
            price = 0.0
            if 'pricelist_id' in res:
                if res['pricelist_id']:
                    date_order_str = datetime.strptime(date_order, DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
                    price = product_pricelist.price_get(cr, uid, [res['pricelist_id']],
                            line.product_id.id, line.product_uom_qty or 1.0, line.partner_id.id or False, {'uom': line.product_id.uom_po_id.id, 'date': date_order_str})[res['pricelist_id']]
                else:
    #                    price = product.standard_price
                    price = line.product_id.standard_price
            else:
                price = line.product_id.standard_price


            item = {
                    'product_id': line.product_id.id,
                    'qty': line.product_uom_qty,
                    'price': price,
                    'subtotal': price * line.product_uom_qty
                }
            if line.product_id:
                items.append(item)


        res.update(line_ids=items)
        return res
    
    def wkf_confirm_order(self, cr, uid, ids, context):
        vals = {}
        purchase_obj = self.pool.get('purchase.order')
        purchase_line_obj = self.pool.get('purchase.order.line')
        product_uom = self.pool.get('product.uom')
        product_product = self.pool.get('product.product')
        res_partner = self.pool.get('res.partner')
        todo = []
        supplierinfo = False

        for po in self.browse(cr, uid, ids):
            vals = {
                'partner_id': po.partner_id.id,
                'date_order':  po.date_order,
                'picking_type_id':po.picking_type_id.id,
                'location_id': po.location_id.id,
                'invoice_method': 'order',
                'pricelist_id': po.partner_id.property_product_pricelist_purchase and po.partner_id.property_product_pricelist_purchase.id,
                'state': 'confirmed',
                'validator' : uid
                
                
            }
            
            purchase_id = purchase_obj.create(cr, uid, vals, context=context)
                
            
            context_partner = context.copy()
            if po.partner_id.id:
                lang = res_partner.browse(cr, uid, po.partner_id.id).lang
                context_partner.update( {'lang': lang, 'partner_id': po.partner_id.id} )
            
            for  line in po.line_ids:
                if line.qty <= 0:
                    continue
                else:
                    date_order = fields.datetime.now()
                    product = product_product.browse(cr, uid, line.product_id.id, context=context_partner)

                    dummy, name = product_product.name_get(cr, uid, line.product_id.id, context=context_partner)[0]
                    if product.description_purchase:
                        name += '\n' + product.description_purchase
                    precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
                    for supplier in product.seller_ids:
                        if po.partner_id.id and (supplier.name.id == po.partner_id.id):
                            supplierinfo = supplier
                            if supplierinfo.product_uom.id != line.product_uom.id:
                                res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                            min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=line.product_uom.id)
                            if float_compare(min_qty , line.qty, precision_digits=precision) == 1: # If the supplier quantity is greater than entered from user, set minimal.
                                if line.qty:
                                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                                line.qty = min_qty
                    dt = purchase_line_obj._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    values = {
                        'product_id': line.product_id.id,
                        'name': name,
                        'date_planned': dt,
                        'product_qty':  line.qty,
                        'price_unit':line.price,
                        'price_subtotal': line.subtotal,
                        'price_subtotal': line.subtotal,
                        'order_id': purchase_id,
                        'sale_order_id': context['active_id'],
                        'state': 'confirmed',

                    }
                    line_id = self.pool.get('purchase.order.line').create(cr, uid, values, context=context)
    #                self.pool.get('purchase.order.line').action_confirm(cr, uid, [line_id], context)
            # if purchase_id:
            #     purchase_obj.signal_workflow(cr, uid, [purchase_id], 'purchase_confirm')
            #     self.pool.get('sale.order').write(cr, uid, [context['active_id']], {'purchase_id' : purchase_id})
            
        return 


class back_to_back_order_line(osv.osv_memory):
    _name = "back.to.back.order.line"
    _description = "Back to Back Order"
    
    
    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line.price, line.qty, line.product_id, line.back_order_id.partner_id)
            cur = line.back_order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
    
    
    
    def _get_uom_id(self, cr, uid, context=None):
        try:
            proxy = self.pool.get('ir.model.data')
            result = proxy.get_object_reference(cr, uid, 'product', 'product_uom_unit')
            return result[1]
        except Exception, ex:
            return False
    
    _columns = {
        
#        'location_destination_id': fields.many2one('stock.location', 'Stock Destination Location'),
#        'location_id': fields.many2one('stock.location', 'Stock Source Location'),
        'product_id': fields.many2one('product.product', 'Product'),
        'back_order_id': fields.many2one('back.to.back.order', 'Back Order'),
        'qty': fields.float('Quantity'),
        'price': fields.float('Unit Price'),
        'subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
        'taxes_id': fields.many2many('account.tax', 'purchase_order_taxe', 'ord_id', 'tax_id', 'Taxes'),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        
           
    }
    
    
    _defaults = {
        'product_uom' : _get_uom_id,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
