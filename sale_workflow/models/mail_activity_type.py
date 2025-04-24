from odoo import api, fields, models, _


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    category = fields.Selection(selection_add=[('server', 'Server')])   
    stage_id = fields.Many2one('mail.activity.stage', 'From Stage', domain="[('res_model', '=', res_model)]")
    rules = fields.Text(string='Python Rules')