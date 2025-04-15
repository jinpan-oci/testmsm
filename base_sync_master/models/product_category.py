from odoo import _, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    is_category_intended_for_shared_catalog = fields.Boolean(
        string="Shared catalog?", default=False
    )
    base_sync_id = fields.Many2one("base.sync", string="Catalog")

    def publish_catalog(self):
        for record in self:
            if record.is_category_intended_for_shared_catalog:
                record.base_sync_id = self.env["base.sync"].create({"name": _("New")})
                record.base_sync_id.generate_base_sync_lines()
