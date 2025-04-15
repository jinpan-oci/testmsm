from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    service_product_to_preselect = fields.Many2one(
        "product.product",
        string="Service Product to Preselect in Sale Orders",
        config_parameter="mr_store_sale.service_product_to_preselect",
    )
    installation_price_rate = fields.Float(
        string="Installation Price Rate",
        default=0,
        config_parameter="mr_store_sale.installation_price_rate",
    )
    use_update_price_line_wizard = fields.Boolean(
        string="Use Update Price Line Wizard",
        config_parameter="mr_store_sale.use_update_price_line_wizard",
    )
    cerfa_template_id = fields.Many2one(
        comodel_name="sign.template",
        string="Default Cerfa Template",
        config_parameter="mr_store_sale.cerfa_template_id",
        default=False,
    )
