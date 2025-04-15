from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_get_recipients_groups(self, message, model_description, msg_vals=None):
        result = super()._notify_get_recipients_groups(
            message, model_description, msg_vals=msg_vals
        )
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("portal_remover.deactivate_portal")
        ):
            result[0][-1]["has_button_access"] = False
        return result
