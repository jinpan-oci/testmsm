# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountTax(models.Model):
    _inherit = "account.tax"

    generate_sign_document = fields.Boolean(string="Generate Cerfa Document")
