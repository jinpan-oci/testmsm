from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    description_html = fields.Html(string="Description Html", compute="_compute_description_html", store=False)
    description_text = fields.Text(string="Description Text", compute="_compute_description_text", store=False)

    @api.depends("sale_line_ids")
    def _compute_description_html(self):
        for record in self:
            if record.sale_line_ids:
                record.description_html = record.sale_line_ids[0].description_html
            else:
                record.description_html = ""

    @api.depends("sale_line_ids")
    def _compute_description_text(self):
        for record in self:
            if record.sale_line_ids:
                record.description_text = record.sale_line_ids[0].description_text
            else:
                record.description_text = ""
