from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.addons.payment.controllers import portal as payment_portal

class CustomerPortal(payment_portal.PaymentPortal):

    @http.route(['/my/orders/<int:order_id>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None):
        # Call the original method to retain existing functionality
        result = super(CustomerPortal, self).portal_quote_accept(order_id, access_token, name, signature)
        # Add custom functionality here
        if order_id:
            order = request.env['sale.order'].sudo().browse(order_id)
            if order.send_cerfa_after_confirmation and order.check_tva_rate_for_sign():
                mail_id = order.create_wizard_mail(order.env.ref("mr_store_sale.email_template_edi_after_sale_cerfa"))
        return result