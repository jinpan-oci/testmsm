from odoo import _, http
from odoo.addons.sign.controllers.main import Sign
from odoo.http import request


class SignContract(Sign):

    @http.route(
        ["/sign/sign_request_state/<int:request_id>/<token>"],
        type="json",
        auth="public",
    )
    def get_sign_request_state(self, request_id, token):
        result = super().sign(request_id, token)
        sale_order_id = (
            request.env["sale.order"]
            .sudo()
            .search([("sign_request_id", "=", request_id)])
        )
        sign_request_id_obj = sale_order_id.sign_request_id
        attachments = sign_request_id_obj.sudo().completed_document_attachment_ids
        if attachments:
            for att in attachments:
                att.sudo().copy({"res_model": "sale.order", "res_id": sale_order_id.id})
            sale_order_id.sudo().message_post(body=_("Cerfa filled"))
        return result
