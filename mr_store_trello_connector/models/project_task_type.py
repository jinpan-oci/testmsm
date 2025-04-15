from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    is_trello_finished_card = fields.Boolean(string="Is trello finished card")
