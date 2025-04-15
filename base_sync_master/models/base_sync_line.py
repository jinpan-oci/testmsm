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


class BaseSyncLine(models.Model):
    _name = "base.sync.line"
    _description = "Base Sync Lines"
    _order = "sequence asc"

    sequence = fields.Integer(string="Sequence", compute="_compute_sequence")

    name = fields.Char(string="Name", required=True)
    base_sync_id = fields.Many2one("base.sync", string="Base Sync")

    file_data = fields.Binary(string="XLSX/CSV File")
    file_name = fields.Char(string="File Name")
    file_number = fields.Integer(string="File Number")

    @api.depends("name")
    def _compute_sequence(self):
        for record in self:
            record.sequence = (
                ((ORDER.index(record.name) * 100) + record.file_number - 1)
                if record.name in ORDER
                else 10000 + record.file_number
            )
