from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mrstore_quotation_type = fields.Selection(
        selection=[
            ("supply_new", "Supply and installation (new)"),
            ("supply_recon", "Supply and installation (reconditioning)"),
            ("supply_remov", "Removed Supply"),
            ("supply_deliv", "Delivered Supply"),
        ],
        default="supply_recon",
        string="Quotation type",
        help="Select the quotation type you want",
        tracking=True,
    )
