from odoo import models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def _notify_get_recipients_groups(self, message, model_description, msg_vals=None):
        groups = super()._notify_get_recipients_groups(message, model_description, msg_vals=msg_vals)

        if self.move_type != 'entry':
            try:
                customer_portal_group = next(group for group in groups if group[0] == "portal_customer")
            except StopIteration:
                pass
            else:
                access_opt = customer_portal_group[2].setdefault("button_access", {})
                if access_opt.get("title") != _("Download Invoice"):
                    access_opt["title"] = _("Download Invoice")
                    self._portal_ensure_token()
                    access_opt["url"] = '/my/invoices/%s?access_token=%s&report_type=pdf&download=true' % (
                        self.id,
                        self.access_token
                    )

        return groups
