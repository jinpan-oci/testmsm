from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    mrstore_quotation_type = fields.Selection(
        selection=[
            ("supply_new", "Supply and installation (new)"),
            ("supply_recon", "Supply and installation (reconditioning)"),
            ("supply_remov", "Removed Supply"),
            ("supply_deliv", "Delivered Supply"),
        ],
        compute="_compute_quotation_type_selection",
        string="Quotation type",
        help="Get the first quotation type of the corresponding sale order and select it for the quotation",
        readonly=False,
        store=True,
        tracking=True,
    )

    def _compute_quotation_type_selection(self):
        for record in self:
            if (
                record.invoice_line_ids
                and record.invoice_line_ids[0]
                and record.invoice_line_ids[0].sale_line_ids
                and record.invoice_line_ids[0].sale_line_ids[0]
                and record.invoice_line_ids[0]
                .sale_line_ids[0]
                .order_id.mrstore_quotation_type
            ):
                record.mrstore_quotation_type = (
                    record.invoice_line_ids[0]
                    .sale_line_ids[0]
                    .order_id.mrstore_quotation_type
                )
            else:
                record.mrstore_quotation_type = "supply_new"
