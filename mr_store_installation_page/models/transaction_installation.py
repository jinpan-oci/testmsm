from odoo import fields, models


class TransactionInstallation(models.Model):
    _name = "transaction.installation"
    _description = "Transaction Installation"

    sequence = fields.Integer(string="Sequence")
    base_installation_id = fields.Many2one("base.installation", string="Base Installation")
    base_installation_line_ids = fields.Many2many(
        "base.installation.line",
        string="Base Installation Line",
        domain="[('base_installation_id', '=', base_installation_id)]",
        required=True,
    )
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
