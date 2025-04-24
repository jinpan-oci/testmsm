from odoo import models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _notify_get_recipients_groups(self, message, model_description, msg_vals=None):
        groups = super()._notify_get_recipients_groups(message, model_description, msg_vals)

        if not self._context.get("proforma"):
            try:
                customer_portal_group = next(group for group in groups if group[0] == "portal_customer")
            except StopIteration:
                pass

            access_opt = customer_portal_group[2].setdefault("button_access", {})
            if access_opt.get("title") != _("Download Quotation"):
                access_opt["title"] = _("Download Quotation")
                access_token = self._portal_ensure_token()
                access_opt["url"] = '/my/orders/%s?access_token=%s&report_type=pdf&download=true' % (self.id,
                                                                                                     access_token)

        return groups

    def action_quotation_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mr_store_mail_change_button.mail_notification_mr_store_sale_order_layout',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }