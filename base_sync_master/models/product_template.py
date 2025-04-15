from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    image_1920_url = fields.Char(
        string="Image URL", compute="_compute_image_1920_url", store=False
    )

    @api.depends("image_1920")
    def _compute_image_1920_url(self):
        for record in self:
            base_url = (
                record.env["ir.config_parameter"].sudo().get_param("web.base.url")
            )
            record.image_1920_url = (
                f"{base_url}/get_image/product.template/{record.id}/image_1920"
            )
