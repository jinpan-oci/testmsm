from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    deactivate_portal = fields.Boolean(
        string="Deactivate Portal Access",
        config_parameter="portal_remover.deactivate_portal",
    )
