from odoo import fields, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    presentation_before = fields.Html(string="Presentation Before")
    presentation_after = fields.Html(string="Presentation After")
    product_uom_qty = fields.Float(
        string="Qty",
        compute="_compute_product_uom_qty",
        digits="Product Unit of Measure",
        default=1.0,
        store=True,
        readonly=False,
        required=True,
        precompute=True,
    )

    price_unit = fields.Float(
        string="UP",
        compute="_compute_price_unit",
        digits="Product Price",
        store=True,
        readonly=False,
        required=True,
        precompute=True,
    )

    tax_id = fields.Many2many(
        comodel_name="account.tax",
        string="VAT",
        compute="_compute_tax_id",
        store=True,
        readonly=False,
        precompute=True,
        context={"active_test": False},
        check_company=True,
    )

    estimated_time = fields.Float(string="Number of estimated hours", default=0.0)

    use_update_price_line_wizard = fields.Boolean(
        string="Use Update Price Line Wizard",
        compute="_compute_use_update_price_line_wizard",
        store=False,
    )

    def _compute_use_update_price_line_wizard(self):
        for record in self:
            record.use_update_price_line_wizard = (
                record.env["ir.config_parameter"]
                .sudo()
                .get_param("mr_store_sale.use_update_price_line_wizard")
            )
