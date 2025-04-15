from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    transaction_installation_ids = fields.One2many(
        comodel_name="transaction.installation",
        inverse_name="sale_order_id",
        string="Base Installation",
    )

    # create a transaction for each base.installation existing
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for sale_order in res:
            base_installation_ids = self.env["base.installation"].search([])
            for base_installation in base_installation_ids:

                default_line = base_installation.base_installation_line_ids.search([("name", "=", "sans")], limit=1)
                if not default_line:
                    default_line = self.env["base.installation.line"].create(
                        {
                            "name": "sans",
                            "base_installation_id": base_installation.id,
                        }
                    )

                self.env["transaction.installation"].create(
                    {
                        "base_installation_id": base_installation.id,
                        "base_installation_line_ids": [(4, default_line.id)],
                        "sale_order_id": sale_order.id,
                    }
                )
        return res
