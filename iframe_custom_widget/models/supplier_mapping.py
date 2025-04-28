from odoo import models, fields, api


class SupplierMapping(models.Model):
    _name = 'iframe.supplier.mapping'
    _description = 'Hercule Pro Supplier Mapping'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    supplier_code = fields.Char(string='Supplier Code (cat_homolog)', required=True)
    partner_id = fields.Many2one('res.partner', string='Odoo Supplier Contact', required=True,
                                 domain=[('supplier_rank', '>', 0)])
    active = fields.Boolean(default=True)

    @api.depends('supplier_code', 'partner_id')
    def _compute_name(self):
        for record in self:
            if record.supplier_code and record.partner_id.name:
                record.name = f"{record.supplier_code} - {record.partner_id.name}"
            else:
                record.name = record.supplier_code or ''

    _sql_constraints = [
        ('unique_supplier_code', 'unique(supplier_code)', 'This supplier code already exists in the mapping table!')
    ]