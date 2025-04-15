from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    trello_api_key = fields.Char(string="Trello API Key", config_parameter="trello_api_key")
    trello_api_secret = fields.Char(string="Trello API Secret", config_parameter="trello_api_secret")
    trello_token = fields.Char(string="Trello Token", config_parameter="trello_token")
    trello_token_secret = fields.Char(string="Trello Token Secret", config_parameter="trello_token_secret")

    use_only_first_task = fields.Boolean(string="Use only the first Task in orders to create trello cards", config_parameter="use_only_first_task")
