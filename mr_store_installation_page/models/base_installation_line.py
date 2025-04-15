from odoo import fields, models


class BaseInstallationLine(models.Model):
    _name = "base.installation.line"
    _description = "Base Installation Line"
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    base_installation_id = fields.Many2one("base.installation", string="Installation")
