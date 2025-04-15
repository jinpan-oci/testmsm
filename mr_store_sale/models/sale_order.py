from odoo import api, fields, models
from werkzeug.urls import url_encode, url_join


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sign_request_id = fields.Many2one("sign.request", string="Sign Request", readonly=True, copy=False)
    link = fields.Char(string="Link", readonly=True, copy=False)
    send_cerfa_after_confirmation = fields.Boolean(
        string="Send Cerfa after confirmation",
        compute="_compute_check_taxes",
        inverse="_inverse_check_taxes",
        store=True,
    )

    date_order = fields.Datetime(tracking=True)

    # def _find_mail_template(self):
    #     self.ensure_one()
    #     if self.check_tva_rate_for_sign() and not self.send_cerfa_after_confirmation:
    #         return self.env.ref("mr_store_sale.email_template_edi_sale_cerfa", raise_if_not_found=False)
    #     else:
    #         return self._get_confirmation_template()

    def check_tva_rate_for_sign(self):
        for line in self.order_line:
            for tax_id in line.tax_id:
                if tax_id.generate_sign_document:
                    return True
        return False

    # def action_quotation_send(self):
    #     res = super().action_quotation_send()
    #     res["context"]["default_template_id"] = self._find_mail_template().id
    #     if self.check_tva_rate_for_sign() and not self.send_cerfa_after_confirmation:
    #         link, token, signer_request_id = self.generate_token_for_sign()
    #         if signer_request_id and link:
    #             self.sign_request_id = signer_request_id.id
    #             self.link = link
    #     return res

    def generate_token_for_sign(self):
        template_id = self.sudo().env["ir.config_parameter"].get_param("mr_store_sale.cerfa_template_id", False)
        if template_id:
            signer_request_id = self.env["sign.request"].create(
                {
                    "template_id": int(template_id),
                    "subject": "Sign Request",
                    "reference": "SO-Sign-%s" % self.name,
                    "request_item_ids": [
                        (
                            0,
                            0,
                            {
                                "partner_id": self.partner_id.id,
                                "role_id": self.env.ref("sign.sign_item_role_customer").id,
                            },
                        )
                    ],
                }
            )
            signer = signer_request_id.request_item_ids[0]
            expiry_link_timestamp = signer._generate_expiry_link_timestamp()
            url_params = url_encode(
                {
                    "timestamp": expiry_link_timestamp,
                    "exp": signer._generate_expiry_signature(signer.id, expiry_link_timestamp),
                }
            )
            token = signer.sudo().access_token
            link = (
                url_join(
                    signer.get_base_url(),
                    "sign/document/mail/%(request_id)s/%(access_token)s?%(url_params)s"
                    % {
                        "request_id": signer.sign_request_id.id,
                        "access_token": token,
                        "url_params": url_params,
                    },
                ),
            )
            return link[0], token, signer_request_id
        else:
            return False, False, False

    def create_wizard_mail(self, mail_template):
        """Opens a wizard to compose an email, with relevant mail template loaded by default"""
        self.ensure_one()
        lang = self.env.context.get("lang")
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            "default_model": "sale.order",
            "default_res_ids": self.ids,
            "default_template_id": mail_template.id if mail_template else None,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "default_email_layout_xmlid": "mail.mail_notification_layout_with_responsible_signature",
            "proforma": self.env.context.get("proforma", False),
            "force_email": True,
            "model_description": self.with_context(lang=lang).type_name,
        }
        return self.env["mail.compose.message"].with_context(ctx).create({})._action_send_mail()

    def send_email_from_template(self, template_id, record_id):
        template = self.env["mail.template"].browse(template_id)
        if not template:
            raise ValueError("Email template not found")
        mail_id = template.send_mail(record_id, force_send=True)
        print(mail_id)
        return mail_id

    def action_confirm(self):
        for line in self.order_line:
            is_there_service = False
            if line.product_id.type == "service":
                is_there_service = True

        if not is_there_service and self.env["ir.config_parameter"].sudo().get_param("mr_store_sale.service_product_to_preselect"):
            service_article = self.env["product.product"].search(
                [
                    (
                        "id",
                        "=",
                        self.env["ir.config_parameter"].sudo().get_param("mr_store_sale.service_product_to_preselect"),
                    )
                ]
            )
            self.sudo().write(
                {
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": service_article.id,
                                "name": service_article.name,
                                "product_uom_qty": 1,
                                "price_unit": 0,
                            },
                        )
                    ]
                }
            )

        res = super().action_confirm()
        if self.send_cerfa_after_confirmation and self.check_tva_rate_for_sign():
            link, token, signer_request_id = self.generate_token_for_sign()
            if signer_request_id and link:
                self.sign_request_id = signer_request_id.id
                self.link = link
            self.create_wizard_mail(self.env.ref("mr_store_sale.email_template_edi_after_sale_cerfa"))
        return res

    @api.depends("order_line", "order_line.tax_id")
    def _compute_check_taxes(self):
        for record in self:
            send_cerfa = False
            if record.order_line:
                for line in record.order_line:
                    if line.tax_id:
                        for tax_id in line.tax_id:
                            if tax_id.generate_sign_document:
                                send_cerfa = True
                                break
                    if send_cerfa:
                        break
            if send_cerfa:
                record.send_cerfa_after_confirmation = True
            else:
                record.send_cerfa_after_confirmation = False

    def _inverse_check_taxes(self):
        pass
