from odoo import _, api, models, modules


class AccountMoveSend(models.TransientModel):
    _inherit = "account.move.send"

    @api.model
    def _get_mail_layout(self):
        return 'mr_store_mail_change_button.mail_notification_mr_store_sale_order_layout'