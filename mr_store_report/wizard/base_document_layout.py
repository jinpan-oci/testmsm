from odoo import fields, models


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    header = fields.Image(string="PDF header", readonly=False)
    footer = fields.Image(string="PDF footer", readonly=False)
    image_total_saleorder = fields.Image(
        string="Sale Order Total image", readonly=False
    )
    image_google_mark = fields.Binary(string="PDF Google Mark", readonly=False)

    footer_title = fields.Char(string="Footer Title", readonly=False)
    column_1_title = fields.Char(string="Column 1 Title", readonly=False)
    column_1_line_1 = fields.Char(string="Column 1 Line 1", readonly=False)
    column_1_line_2 = fields.Char(string="Column 1 Line 2", readonly=False)
    column_1_line_3 = fields.Char(string="Column 1 Line 3", readonly=False)
    column_1_line_4 = fields.Char(string="Column 1 Line 4", readonly=False)
    column_2_title = fields.Char(string="Column 2 Title", readonly=False)
    column_2_line_1 = fields.Char(string="Column 2 Line 1", readonly=False)
    column_2_line_2 = fields.Char(string="Column 2 Line 2", readonly=False)
    column_2_line_3 = fields.Char(string="Column 2 Line 3", readonly=False)
    column_2_line_4 = fields.Char(string="Column 2 Line 4", readonly=False)
    column_3_title = fields.Char(string="Column 3 Title", readonly=False)
    column_3_line_1 = fields.Char(string="Column 3 Line 1", readonly=False)
    column_3_line_2 = fields.Char(string="Column 3 Line 2", readonly=False)
    column_3_line_3 = fields.Char(string="Column 3 Line 3", readonly=False)
    column_3_line_4 = fields.Char(string="Column 3 Line 4", readonly=False)
    footer_line_1 = fields.Char(string="Footer Line 1", readonly=False)
    footer_line_2 = fields.Char(string="Footer Line 2", readonly=False)


class BaseDocumentLayout(models.TransientModel):
    _name = "base.document.layout"
    _inherit = "base.document.layout"

    header = fields.Binary(related="company_id.header", readonly=False)
    footer = fields.Binary(related="company_id.footer", readonly=False)
    image_total_saleorder = fields.Binary(
        related="company_id.image_total_saleorder", readonly=False
    )
    image_google_mark = fields.Binary(
        related="company_id.image_google_mark", readonly=False
    )

    footer_title = fields.Char(related="company_id.footer_title", readonly=False)
    column_1_title = fields.Char(related="company_id.column_1_title", readonly=False)
    column_1_line_1 = fields.Char(related="company_id.column_1_line_1", readonly=False)
    column_1_line_2 = fields.Char(related="company_id.column_1_line_2", readonly=False)
    column_1_line_3 = fields.Char(related="company_id.column_1_line_3", readonly=False)
    column_1_line_4 = fields.Char(related="company_id.column_1_line_4", readonly=False)
    column_2_title = fields.Char(related="company_id.column_2_title", readonly=False)
    column_2_line_1 = fields.Char(related="company_id.column_2_line_1", readonly=False)
    column_2_line_2 = fields.Char(related="company_id.column_2_line_2", readonly=False)
    column_2_line_3 = fields.Char(related="company_id.column_2_line_3", readonly=False)
    column_2_line_4 = fields.Char(related="company_id.column_2_line_4", readonly=False)
    column_3_title = fields.Char(related="company_id.column_3_title", readonly=False)
    column_3_line_1 = fields.Char(related="company_id.column_3_line_1", readonly=False)
    column_3_line_2 = fields.Char(related="company_id.column_3_line_2", readonly=False)
    column_3_line_3 = fields.Char(related="company_id.column_3_line_3", readonly=False)
    column_3_line_4 = fields.Char(related="company_id.column_3_line_4", readonly=False)
    footer_line_1 = fields.Char(related="company_id.footer_line_1", readonly=False)
    footer_line_2 = fields.Char(related="company_id.footer_line_2", readonly=False)
