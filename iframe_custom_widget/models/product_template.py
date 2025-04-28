from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_source = fields.Char(string='Product Source', readonly=True, default=False)