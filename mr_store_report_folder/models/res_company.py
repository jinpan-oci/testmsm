from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    vat_pdf = fields.Binary(string="VAT PDF")

    help_qr_code = fields.Binary(string="Help QR Code")

    qr_code_1 = fields.Binary(string="QR Code 1 - 8eme")
    qr_code_2 = fields.Binary(string="QR Code 2 - 3eme")
    qr_code_3 = fields.Binary(string="QR Code 3 - Aix")

    guard_page = fields.Boolean(string="Guard Page", default=True)
    guard_page_steps = fields.Boolean(string="Guard Page Steps", default=True)
    guard_page_supplier = fields.Boolean(string="Guard Page Supplier", default=True)
    guard_page_table_purchase = fields.Boolean(string="Guard Page Table Purchase", default=True)
    margin_page = fields.Boolean(string="Margin Page", default=True)
    installation_sheet = fields.Boolean(string="Installation Sheet", default=True)
    installation_sheet_stock_header = fields.Boolean(string="Installation Sheet Stock", default=True)
    installation_sheet_stock = fields.Boolean(string="Installation Sheet Stock Header", default=True)
    installation_sheet_manual = fields.Boolean(string="Installation Sheet Manual", default=True)
    installation_sheet_supplier = fields.Boolean(string="Installation Sheet Supplier", default=True)
    installation_sheet_google_review = fields.Boolean(string="Installation Sheet Google Review - Marseille", default=False)
    installation_sheet_google_street = fields.Boolean(string="Installation Sheet Google Street", default=True)
    verbal_report = fields.Boolean(string="Verbal Report", default=True)
    verbal_report_installer = fields.Boolean(string="Verbal Report Installer", default=True)
    verbal_report_google_review = fields.Boolean(string="Verbal Report Google Review - Marseille", default=False)
    installation_images = fields.Boolean(string="Installation Images", default=True)
    installation_images_before_install = fields.Boolean(string="Installation Images Before Install", default=True)
    installation_images_with_3d = fields.Boolean(string="Installation Images With 3D", default=True)
    installation_images_measurements = fields.Boolean(string="Installation Images Measurements", default=True)
    installation_images_other = fields.Boolean(string="Installation Images Other", default=True)
    tva_pdf = fields.Boolean(string="TVA PDF", default=True)

    # -------------------------------------------------------------------------------------------------------------
    # OLD - DO NOT USE FROM NOW ON - FOR MIGRATION PURPOSES ONLY --------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------

    gsc_pdf = fields.Binary(string="GCS PDF")
    guarantee_contract_pdf = fields.Binary(string="Guarantee Contract PDF")
    guarantee_book_pdf = fields.Binary(string="Guarantee Book PDF")
