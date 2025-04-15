from odoo import models, fields, api

class ModuleUpdateTag(models.Model):
    _name = 'module.update.tag'
    _description = 'Update Tag: contain tags for modules to update'

    name = fields.Char(string='Name')
    module_updater_ids = fields.Many2many('module.updater', string='Modules Updater')