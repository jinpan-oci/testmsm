from odoo import fields, models


class HerculeLabel(models.Model):
    _name = "hercule.label"
    _description = "Hercule Description"
    _sql_constraints = [
        ("unique_name", "unique(name)", "This name already exists"),
        ("unique_label", "unique(name)", "This label already exists"),
    ]

    name = fields.Html(string="Description")  # , compute="_compute_name"

    origin_label = fields.Html(string="Origin Description", readonly=True)
    custom_label = fields.Html(string="Custom label old", readonly=True)  # OLD DO NOT USE FROM NOW ON - FOR MIGRATION PURPOSES ONLY
    show_price = fields.Boolean(string="Show Price", default=False)

    hercule_product_ids = fields.One2many("hercule.product", "label_id", string="Hercule Products")

    show_origin = fields.Boolean(string="Show Origin Description", compute="_compute_show_origin", store=False)

    # @api.depends("origin_label", "name")
    # def _compute_name(self):
    #     for record in self:
    #         if record.name:
    #             record.name = record.name[:47] + "..." if len(record.name) > 50 else record.name
    #         elif record.origin_label:
    #             record.name = record.origin_label[:47] + "..." if len(record.origin_label) > 50 else record.origin_label
    #         else:
    #             record.name = ""

    def _compute_show_origin(self):
        for record in self:
            record.show_origin = self.env["ir.config_parameter"].sudo().get_param("autocomplete_desc_matrix", False)
