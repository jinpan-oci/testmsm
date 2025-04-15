import hashlib

from odoo import api, fields, models

# 305b2653b85b8f580a869ef6637d3191 md5 desired password
# 098f6bcd4621d373cade4e832627b4f6 md5 for 'test'


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    iframe_host = fields.Char(
        "Iframe Host",
        config_parameter="iframe_host",
        default="https://mrstore-preprod.herculepro.com",
    )
    iframe_sub_url = fields.Char("Iframe Sub Url", config_parameter="iframe_sub_url", default="/hpv5/wizapi?")
    iframe_api_tool_id = fields.Char("Iframe API Tool ID", config_parameter="iframe_api_tool_id", default="0x10060")
    iframe_usr = fields.Char("Iframe User", config_parameter="iframe_usr")
    iframe_pwd = fields.Char(
        "Iframe Password",
        config_parameter="iframe_pwd",
        compute="_compute_pwd",
        store=True,
    )
    iframe_external_tool_id = fields.Char(
        "Iframe External Tool ID",
        config_parameter="iframe_external_tool_id",
        default="0x10060",
    )
    iframe_md5_pwd = fields.Char(
        "Iframe MD5 Password",
        config_parameter="iframe_md5_pwd",
        compute="_compute_md5_pwd",
        store=True,
    )
    iframe_change_pwd = fields.Boolean("Change Password", default=False, store=False)
    hp5_default_route_id = fields.Many2one("stock.route", "Default MTO Routes", config_parameter="hp5_default_route_id")

    show_catalog_fart_code = fields.Boolean(
        string="Show Catalog and Fart Code",
        related="company_id.show_catalog_fart_code",
        readonly=False,
    )

    autocomplete_desc_matrix = fields.Boolean(string="Auto Completion", config_parameter="autocomplete_desc_matrix")

    @api.depends("iframe_change_pwd")
    def _compute_pwd(self):
        for record in self:
            if record.iframe_change_pwd:
                record.iframe_pwd = ""

    @api.depends("iframe_pwd")
    def _compute_md5_pwd(self):
        for record in self:
            if record.iframe_pwd:
                pwd = record.iframe_pwd
                pwd = hashlib.md5(pwd.encode()).hexdigest()
                record.iframe_md5_pwd = pwd
            else:
                record.iframe_md5_pwd = ""

    # ---------------------------------------------------------
    # OLD - DO NOT USE FROM NOW ON - FOR MIGRATION PURPOSES ---
    # ---------------------------------------------------------

    hp5_default_categ_id = fields.Many2one("product.category", "Default Category", config_parameter="hp5_default_categ_id")
