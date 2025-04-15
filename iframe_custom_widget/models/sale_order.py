from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    iframe_rul = fields.Text(string="Iframe URL")

    show_catalog_fart_code = fields.Boolean(
        string="Show Catalog and Fart Code",
        compute="_compute_show_catalog_fart_code",
        store=False,
    )

    @api.depends("company_id.show_catalog_fart_code")
    def _compute_show_catalog_fart_code(self):
        self.show_catalog_fart_code = self.company_id.show_catalog_fart_code
