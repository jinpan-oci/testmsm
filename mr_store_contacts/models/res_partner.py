from datetime import datetime

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    residence_name = fields.Char("Residence Name", required=False)
    residence_number = fields.Char("Residence Number", required=False)
    appartment_number = fields.Char("Appartment Number", required=False)
    floor_number = fields.Char("Floor Number", required=False)
    portal_code = fields.Char("Portal Code", required=False)
    entry_code = fields.Char("Door Code", required=False)

    house_type = fields.Selection(
        string="House Type",
        selection=[
            ("house", "House"),
            ("building", "Building"),
            ("residence", "Residence"),
        ],
        required=False,
    )

    original_creation_date = fields.Date(
        "Original Creation Date", default=datetime.now(), required=False
    )
