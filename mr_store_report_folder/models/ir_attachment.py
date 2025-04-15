from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    photo_use_type = fields.Selection(
        [
            ("before_installation", "Photo Before Installation"),
            ("with_3d", "Photo With 3D"),
            ("mesures", "Mesures Drawings"),
            ("other", "Other"),
        ],
        string="Photo Use Type",
        default="other",
    )
