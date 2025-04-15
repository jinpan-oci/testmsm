from odoo import fields, models


class HerculeLabel(models.Model):
    _name = "hercule.title"
    _description = "Hercule Title"
    _sql_constraints = [
        ("unique_name", "unique(name)", "This name already exists"),
        ("unique_title", "unique(name)", "This title already exists"),
    ]

    name = fields.Html(string="Custom Title")
    origin_title = fields.Html(string="Origin Title", readonly=True)
    custom_title = fields.Html(string="Custom Title old", readonly=True)  # OLD DO NOT USE FROM NOW ON - FOR MIGRATION PURPOSES ONLY

    hercule_product_ids = fields.One2many("hercule.product", "title_id", string="Hercule Products")

    show_origin = fields.Boolean(string="Show Origin Label", compute="_compute_show_origin", store=False)

    # @api.depends("origin_title", "name")
    # def _compute_name(self):
    #     for record in self:
    #         if record.name:
    #             record.name = record.name[:47] + "..." if len(record.name) > 50 else record.name
    #         elif record.origin_title:
    #             record.name = record.origin_title[:47] + "..." if len(record.origin_title) > 50 else record.origin_title
    #         else:
    #             record.name = ""

    def _compute_show_origin(self):
        for record in self:
            record.show_origin = self.env["ir.config_parameter"].sudo().get_param("autocomplete_desc_matrix", False)
