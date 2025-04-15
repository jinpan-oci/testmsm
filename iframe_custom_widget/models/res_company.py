from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    show_catalog_fart_code = fields.Boolean(string="Show Catalog and Fart Code")