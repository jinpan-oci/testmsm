from odoo import api, fields, models

ORDER = [
    "product.category",
    "product.attribute",
    "uom.category",
    "product.tag",
    "product.template",
    "product.template.attribute.line",
    "res.partner.category",
    "res.country",
    "res.partner",
    "product.supplierinfo",
    "product.pricelist",
]


class BaseSyncTemplateLine(models.Model):
    _name = "base.sync.template.line"
    _description = "Base Sync Template Line"
    _order = "sequence asc"

    sequence = fields.Integer(
        string="Sequence", compute="_compute_sequence", store="False"
    )
    base_sync_template_id = fields.Many2one(
        "base.sync.template", string="Base Sync Template"
    )
    ir_exports_id = fields.Many2one("ir.exports", string="Exports")

    @api.depends("ir_exports_id")
    def _compute_sequence(self):
        for record in self:
            record.sequence = (
                ORDER.index(record.ir_exports_id.resource)
                if record.ir_exports_id.resource in ORDER
                else 100
            )
