from odoo import fields, models


class HerculeProduct(models.Model):
    _name = "hercule.product"
    _description = "Hercule products model"
    _sql_constraints = [
        ("unique_product", "unique(name)", "This product already exists"),
    ]

    name = fields.Char(string="Product Code")
    sequence = fields.Integer(string="Sequence order in product description")

    label_id = fields.Many2one("hercule.label", string="Label")
    title_id = fields.Many2one("hercule.title", string="Title")
