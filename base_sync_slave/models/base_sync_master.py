from odoo import fields, models


class BaseSyncMaster(models.Model):

    _name = "base.sync.master"
    _description = "Base Sync Master"

    name = fields.Char(string="Name", required=True)
    master_url = fields.Char(string="Master URL", required=True)
    master_db = fields.Char(string="Master DB", required=True)
    master_user = fields.Char(string="Master User", required=True)
    master_api_key = fields.Char(string="Master API Key", required=True)
    notification_follower_ids = fields.Many2many(
        "res.partner", string="Update Notification Followers"
    )
