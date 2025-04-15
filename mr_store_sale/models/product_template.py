from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    presentation_before = fields.Html(string="saleorder prefix", required=False)
    presentation_after = fields.Html(string="saleorder suffix", required=False)
