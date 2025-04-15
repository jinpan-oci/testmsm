from odoo import fields, models


class ModuleUpdater(models.Model):
    _name = "module.updater"
    _description = "Module Updater: contain servers list and modules to update"

    module_updater_lines = fields.One2many("module.updater.line", "module_updater_id", string="Module Updater Line")
    name = fields.Char(string="Name")
    update_ids = fields.Many2many("module.update.tag", string="Modules to Update")
    install_ids = fields.Many2many("module.install.tag", string="Modules to Install")

    def update_all(self):
        for record in self:
            for line in record.module_updater_lines:
                line.update_module()

    def install_all(self):
        for record in self:
            for line in record.module_updater_lines:
                line.install_module()
