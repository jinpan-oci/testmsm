from odoo import models, fields, api

class ModuleInstallTag(models.Model):
    _name = 'module.install.tag'
    _description = 'Install Tag: contain tags for modules to install'

    name = fields.Char(string='Name')
    module_updater_ids = fields.Many2many('module.updater', string='Modules Updater')