from odoo import _, api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    residence_name = fields.Char(
        "Residence Name", related="partner_id.residence_name", readonly=True, store=True
    )

    residence_number = fields.Char(
        "Residence Number",
        related="partner_id.residence_number",
        readonly=True,
        store=True,
    )

    appartment_number = fields.Char(
        "Appartment Number",
        related="partner_id.appartment_number",
        readonly=True,
        store=True,
    )

    floor_number = fields.Char(
        "Floor Number", related="partner_id.floor_number", readonly=True, store=True
    )

    portal_code = fields.Char(
        "Portal Code", related="partner_id.portal_code", readonly=True, store=True
    )

    entry_code = fields.Char(
        "Door Code", related="partner_id.entry_code", readonly=True, store=True
    )

    house_type = fields.Selection(
        string="House Type", related="partner_id.house_type", readonly=True, store=True
    )

    short_name = fields.Char(
        "Short Name", compute="_compute_short_name", readonly=True, store=True
    )

    @api.depends(
        "residence_name",
        "residence_number",
        "appartment_number",
        "floor_number",
        "portal_code",
        "entry_code",
        "house_type",
    )
    def _compute_short_name(self):
        for record in self:
            short_name = ""
            if record.house_type:
                if record.house_type == "residence":
                    short_name += _("Residence: ")
                elif record.house_type == "house":
                    short_name += _("House: ")
                elif record.house_type == "building":
                    short_name += _("Building: ")
            if record.residence_name:
                short_name += record.residence_name + ", "
            if record.residence_number:
                short_name += "n° " + record.residence_number + "\n"
            if record.appartment_number:
                short_name += "Apt " + record.appartment_number + ", "
            if record.floor_number:
                short_name += _("Floor ") + record.floor_number + "\n"
            if record.portal_code:
                short_name += _("Portal Code: ") + record.portal_code + "\n"
            if record.entry_code:
                short_name += _("Door Code: ") + record.entry_code + "\n"
            record.short_name = short_name
