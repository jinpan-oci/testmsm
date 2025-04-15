from odoo import fields, models


class BaseSyncTemplate(models.Model):
    _name = "base.sync.template"
    _description = "Base Sync Template"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    base_sync_template_line_ids = fields.One2many(
        comodel_name="base.sync.template.line",
        inverse_name="base_sync_template_id",
        string="Template Line",
    )
    is_default_template = fields.Boolean("Is default template ?", default=False)
    csv_or_xlsx = fields.Selection(
        [("csv", "CSV"), ("xlsx", "XLSX")], string="File Type", default="xlsx"
    )
