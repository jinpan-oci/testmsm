from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    iframe_url = fields.Text(string="Iframe URL")
    product_source = fields.Char(string='Product Source')