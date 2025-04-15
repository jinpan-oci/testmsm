import base64
from io import BytesIO

import qrcode
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    trello_idcardsource = fields.Char(string="Trello id card source")
    trello_url = fields.Html(string="Trello url")
    trello_installers_number = fields.Char(
        string="(P) Trello Installers Number",
        compute="_compute_trello_installers_number",
        store=False,
    )
    trello_duration = fields.Char(
        string="(H) Trello Duration in hours",
        compute="_compute_trello_duration",
        store=False,
    )
    trello_pax_number_for_forwarding = fields.Char(
        string="(AP) Trello Pax Number for Forwarding",
        compute="_compute_trello_pax_number_for_forwarding",
        store=False,
    )
    trello_forwarding_duration = fields.Char(
        string="(AH) Trello Forwarding Duration in hours",
        compute="_compute_trello_forwarding_duration",
        store=False,
    )
    trello_L = fields.Char(string="Trello L", compute="_compute_trello_L", store=False)
    trello_rdv_confirmed = fields.Boolean(string="Trello rdv confirmed")

    trello_qr_code = fields.Binary("QR Code", compute="generate_trello_qr_code")
    is_trello_finished_card = fields.Boolean(
        string="Is trello finished", related="stage_id.is_trello_finished_card"
    )

    @api.depends("trello_idcardsource")
    def generate_trello_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data("https://trello.com/search?q=")
                qr.add_data(rec.trello_idcardsource)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({"trello_qr_code": qr_image})

    def _compute_trello_installers_number(self):
        for rec in self:
            if rec.sale_order_id:
                rec.trello_installers_number = rec.sale_order_id.P
            else:
                rec.trello_installers_number = "0"

    def _compute_trello_duration(self):
        for rec in self:
            if rec.sale_order_id:
                rec.trello_duration = rec.sale_order_id.H
            else:
                rec.trello_duration = "0"

    def _compute_trello_pax_number_for_forwarding(self):
        for rec in self:
            if rec.sale_order_id:
                rec.trello_pax_number_for_forwarding = rec.sale_order_id.AP
            else:
                rec.trello_pax_number_for_forwarding = "0"

    def _compute_trello_forwarding_duration(self):
        for rec in self:
            if rec.sale_order_id:
                rec.trello_forwarding_duration = rec.sale_order_id.AH
            else:
                rec.trello_forwarding_duration = "0"

    def _compute_trello_L(self):
        for rec in self:
            if rec.sale_order_id:
                rec.trello_L = rec.sale_order_id.L
            else:
                rec.trello_L = "0"
