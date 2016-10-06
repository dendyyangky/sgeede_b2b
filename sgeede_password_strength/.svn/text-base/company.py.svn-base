from openerp.osv import fields,osv

class res_company(osv.osv):
    _inherit = "res.company"
    _columns = {
        'level': fields.selection([(1,'Weak'),(2,'Good'),(3,'Very Good'),(4,'Strong'),(5,'Very Strong')],'Level '),
        }
    _defaults = {
#       'level' : lambda *a : 'weak',#untuk default saat peratma running
        }
