from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    pu_position_selection = fields.Selection(
        selection=[
            ("with_pu_top", "With PU on top"),
            ("with_pu_bot", "With PU on bottom"),
            ("without_pu", "Without PU"),
        ],
        string="Position of PU",
        default="with_pu_top",
    )

    simple_report = fields.Boolean(string="Simple Report", default=False)
