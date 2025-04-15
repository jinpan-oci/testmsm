from odoo import fields, models


class BaseSyncSlaves(models.Model):
    _name = "base.sync.slaves"
    _description = "Base Sync Slaves"

    name = fields.Char(string="Name", required=True)
    slave_url = fields.Char(string="URL", required=True)
