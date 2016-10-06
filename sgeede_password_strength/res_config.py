from openerp.osv import fields,osv
   
SELECTION_LIST = [
    (1,'Weak'),
    (2,'Good'),
    (3,'Very Good'),
    (4,'Strong'),
    (5,'Very Strong')
]

class password_strength(osv.osv_memory):
    _name = "password.strength"
    _inherit = "res.config.settings"
    _columns = {
        'company_id': fields.many2one('res.company', string="Company", required=True),
        'level' : fields.related('company_id', 'level', type="selection", selection=SELECTION_LIST, string="Level"),
        }
    def on_change_company_id(self, cr, uid, ids, company_id, context=None):
        website_data = self.pool.get('res.company').read(cr, uid, [company_id], [], context=context)[0]
        values = {}
        for fname, v in website_data.items():
            if fname in self._columns:
                values[fname] = v[0] if v and self._columns[fname]._type == 'many2one' else v
        return {'value' : values}

    def create(self, cr, uid, vals, context=None):
        config_id = super(password_strength, self).create(cr, uid, vals, context=context)
        self.write(cr, uid, config_id, vals, context=context)
        return config_id

    _defaults = {
        'company_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr,uid,uid).company_id.id,
    }