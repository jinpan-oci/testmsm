from odoo import fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    pu_position_selection = fields.Selection(
        selection=[("with_pu", "With PU"), ("without_pu", "Without PU")],
        string="Position of PU",
        compute="_compute_pu_position_selection",
    )

    def _compute_pu_position_selection(self):
        for record in self:
            if (
                record.invoice_line_ids
                and record.invoice_line_ids[0]
                and record.invoice_line_ids[0].sale_line_ids
                and record.invoice_line_ids[0].sale_line_ids[0]
                and record.invoice_line_ids[0]
                .sale_line_ids[0]
                .order_id.pu_position_selection
            ):
                sale_order_pu_position = (
                    record.invoice_line_ids[0]
                    .sale_line_ids[0]
                    .order_id.pu_position_selection
                )
                if sale_order_pu_position == "with_pu_top":
                    record.pu_position_selection = "with_pu"
                elif sale_order_pu_position == "with_pu_bot":
                    record.pu_position_selection = "with_pu"
                else:
                    record.pu_position_selection = "without_pu"
            else:
                record.pu_position_selection = "with_pu"
