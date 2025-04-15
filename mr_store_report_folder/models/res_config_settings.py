from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    google_api_key = fields.Char(string="Google Maps API Key", config_parameter="google_api_key")

    vat_pdf = fields.Binary(string="VAT PDF", related="company_id.vat_pdf", readonly=False)

    help_qr_code = fields.Binary(string="Help QR Code", related="company_id.help_qr_code", readonly=False)

    qr_code_1 = fields.Binary(string="QR Code 1 - 8ème", related="company_id.qr_code_1", readonly=False)
    qr_code_2 = fields.Binary(string="QR Code 2 - 3ème", related="company_id.qr_code_2", readonly=False)
    qr_code_3 = fields.Binary(string="QR Code 3 - Aix", related="company_id.qr_code_3", readonly=False)

    guard_page = fields.Boolean(string="Guard Page", related="company_id.guard_page", readonly=False)
    guard_page_steps = fields.Boolean(string="Guard Page Steps", related="company_id.guard_page_steps", readonly=False)
    guard_page_supplier = fields.Boolean(string="Guard Page Supplier", related="company_id.guard_page_supplier", readonly=False)
    guard_page_table_purchase = fields.Boolean(string="Guard Page Table Purchase", related="company_id.guard_page_table_purchase", readonly=False)
    margin_page = fields.Boolean(string="Margin Page", related="company_id.margin_page", readonly=False)
    installation_sheet = fields.Boolean(string="Installation Sheet", related="company_id.installation_sheet", readonly=False)
    installation_sheet_stock_header = fields.Boolean(string="Installation Sheet Stock Header", related="company_id.installation_sheet_stock_header", readonly=False)
    installation_sheet_stock = fields.Boolean(string="Installation Sheet Stock", related="company_id.installation_sheet_stock", readonly=False)
    installation_sheet_manual = fields.Boolean(string="Installation Sheet Manual", related="company_id.installation_sheet_manual", readonly=False)
    installation_sheet_supplier = fields.Boolean(string="Installation Sheet Supplier", related="company_id.installation_sheet_supplier", readonly=False)
    installation_sheet_google_review = fields.Boolean(string="Installation Sheet Google Review", related="company_id.installation_sheet_google_review", readonly=False)
    installation_sheet_google_street = fields.Boolean(string="Installation Sheet Google Street", related="company_id.installation_sheet_google_street", readonly=False)
    verbal_report = fields.Boolean(string="Verbal Report", related="company_id.verbal_report", readonly=False)
    verbal_report_installer = fields.Boolean(string="Verbal Report Installer", related="company_id.verbal_report_installer", readonly=False)
    verbal_report_google_review = fields.Boolean(string="Verbal Report Google Review", related="company_id.verbal_report_google_review", readonly=False)
    installation_images = fields.Boolean(string="Installation Images", related="company_id.installation_images", readonly=False)
    installation_images_before_install = fields.Boolean(
        string="Installation Images Before Install", related="company_id.installation_images_before_install", readonly=False
    )
    installation_images_with_3d = fields.Boolean(string="Installation Images With 3D", related="company_id.installation_images_with_3d", readonly=False)
    installation_images_measurements = fields.Boolean(string="Installation Images Measurements", related="company_id.installation_images_measurements", readonly=False)
    installation_images_other = fields.Boolean(string="Installation Images Other", related="company_id.installation_images_other", readonly=False)
    tva_pdf = fields.Boolean(string="TVA PDF", related="company_id.tva_pdf", readonly=False)

    # -------------------------------------------------------------------------------------------------------------
    # OLD - DO NOT USE FROM NOW ON - FOR MIGRATION PURPOSES ONLY --------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------

    gsc_pdf = fields.Binary(string="GCS PDF", related="company_id.gsc_pdf", readonly=False)
    guarantee_contract_pdf = fields.Binary(
        string="Guarantee Contract PDF",
        related="company_id.guarantee_contract_pdf",
        readonly=False,
    )
    guarantee_book_pdf = fields.Binary(
        string="Guarantee Book PDF",
        related="company_id.guarantee_book_pdf",
        readonly=False,
    )

    map_view_type_1 = fields.Selection(
        [
            ("streetview", "Street View"),
            ("staticmap", "Static Map"),
        ],
        string="Map View Type 1",
        default="streetview",
        required=True,
        config_parameter="map_view_type_1",
    )
    map_view_type_2 = fields.Selection(
        [
            ("streetview", "Street View"),
            ("staticmap", "Static Map"),
        ],
        string="Map View Type 2",
        default="staticmap",
        required=True,
        config_parameter="map_view_type_2",
    )
    map_view_type_3 = fields.Selection(
        [
            ("streetview", "Street View"),
            ("staticmap", "Static Map"),
        ],
        string="Map View Type 3",
        default="staticmap",
        required=True,
        config_parameter="map_view_type_3",
    )
    map_view_type_4 = fields.Selection(
        [
            ("streetview", "Street View"),
            ("staticmap", "Static Map"),
        ],
        string="Map View Type 4",
        default="staticmap",
        required=True,
        config_parameter="map_view_type_4",
    )
    map_type_1 = fields.Selection(
        [
            ("hybrid", "Hybrid"),
            ("none", "None"),
        ],
        string="Map Type 1",
        default="none",
        required=True,
        config_parameter="map_type_1",
    )
    map_type_2 = fields.Selection(
        [
            ("hybrid", "Hybrid"),
            ("none", "None"),
        ],
        string="Map Type 2",
        default="hybrid",
        required=True,
        config_parameter="map_type_2",
    )
    map_type_3 = fields.Selection(
        [
            ("hybrid", "Hybrid"),
            ("none", "None"),
        ],
        string="Map Type 3",
        default="hybrid",
        required=True,
        config_parameter="map_type_3",
    )
    map_type_4 = fields.Selection(
        [
            ("hybrid", "Hybrid"),
            ("none", "None"),
        ],
        string="Map Type 4",
        default="none",
        required=True,
        config_parameter="map_type_4",
    )
    map_zoom_1 = fields.Integer(string="Map Zoom 1", default=0, required=True, config_parameter="map_zoom_1")
    map_zoom_2 = fields.Integer(string="Map Zoom 2", default=18, required=True, config_parameter="map_zoom_2")
    map_zoom_3 = fields.Integer(string="Map Zoom 3", default=14, required=True, config_parameter="map_zoom_3")
    map_zoom_4 = fields.Integer(string="Map Zoom 4", default=14, required=True, config_parameter="map_zoom_4")
