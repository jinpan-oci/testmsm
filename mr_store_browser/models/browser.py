from odoo import fields, models


class Browser(models.Model):

    _name = "browser"
    _description = "Browser"

    name = fields.Char(string="Name", required=True)
