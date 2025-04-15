# Copyright irokoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleServiceUpdate(models.TransientModel):
    _name = "sale.order.line.service.update.wizard"
    _description = "update price line Wizard"

    line_id = fields.Many2one("sale.order.line", string="Order line")
    estimated_time = fields.Float(string="Number of estimated hours", required=True)
    rate_price = fields.Float(string="Hour price rate", required=True)
    actual_unit_price = fields.Float(string="Actual unit price", required=True)
    original_unit_price = fields.Float(string="Origin Unit price", required=True)
    new_unit_price = fields.Float(
        string="New unit price", compute="_compute_new_unit_price"
    )
    hide_service = fields.Boolean(string="Hide service", default=True)

    # computes
    @api.depends("estimated_time", "rate_price", "original_unit_price")
    def _compute_new_unit_price(self):
        for rec in self:
            rec.new_unit_price = (
                rec.original_unit_price + rec.estimated_time * rec.rate_price
            )

    # methods
    @api.model
    def default_get(self, fields):
        rec = super().default_get(fields)
        active_id = self.env.context.get("active_id", False)
        sol = self.env["sale.order.line"].browse(active_id)
        rec.update(
            {
                "rate_price": self.env["ir.config_parameter"]
                .sudo()
                .get_param("mr_store_sale.installation_price_rate"),
                "line_id": active_id,
                "estimated_time": sol.estimated_time,
                "original_unit_price": sol.product_id.lst_price,
                "actual_unit_price": sol.price_unit,
            }
        )
        return rec

    def update_service_line(self):
        self.ensure_one()
        if self.hide_service:
            self.line_id.write({"price_unit": self.original_unit_price})
            self.line_id.write(
                {
                    "price_unit": self.new_unit_price,
                    "estimated_time": self.estimated_time,
                }
            )
        else:
            self.line_id.write({"price_unit": self.original_unit_price})
            service_article = self.env["product.product"].search(
                [
                    (
                        "id",
                        "=",
                        self.env["ir.config_parameter"]
                        .sudo()
                        .get_param("mr_store_sale.service_product_to_preselect"),
                    )
                ]
            )
            self.line_id.order_id.write(
                {
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": service_article.id,
                                "name": service_article.name,
                                "product_uom_qty": 1,
                                "price_unit": self.rate_price * self.estimated_time,
                                "estimated_time": self.estimated_time,
                            },
                        )
                    ]
                }
            )
            self.line_id.write({"estimated_time": self.estimated_time})
