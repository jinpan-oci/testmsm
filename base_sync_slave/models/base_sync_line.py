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

    name = fields.Char(string="Name")
    sequence = fields.Integer(
        string="Sequence", compute="_compute_sequence", store="False"
    )
    base_sync_id = fields.Many2one("base.sync", string="Catalog")
    file_data = fields.Binary(string="XLSX/CSV File")
    file_name = fields.Char(string="File Name")
    file_number = fields.Integer(string="File Number")
    error_list = fields.Text(string="Error List")
    is_imported = fields.Boolean(string="Is Imported ?", default=False)

    @api.depends("name")
    def _compute_sequence(self):
        for record in self:
            record.sequence = (
                ((ORDER.index(record.name) * 10) + record.file_number - 1)
                if record.name in ORDER
                else 1000
            )

    def import_one(self):
        for record in self:
            if record.base_sync_id.csv_or_xlsx == "csv":
                record.base_sync_id.with_context(lang="en_US").import_csv(record)
            elif record.base_sync_id.csv_or_xlsx == "xlsx":
                record.base_sync_id.with_context(lang="en_US").import_xlsx(record)
