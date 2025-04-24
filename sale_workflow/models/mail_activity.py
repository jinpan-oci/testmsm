from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    stage_id = fields.Many2one('mail.activity.stage', 'Current Stage')
    rules = fields.Text('Rules', related='activity_type_id.rules')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(MailActivity, self).create(vals_list)
        for activity in res:
            activity.stage_id = activity.activity_type_id.stage_id
        return res

    def set_next_stage(self):
        self.ensure_one()
        record = self.env[self.res_model].browse(self.res_id)

        if self.stage_id:
            if self.stage_id.wait_for_all_activities:
                activity_ids = record.activity_ids.filtered(lambda x: x.stage_id == self.stage_id)
                if activity_ids:
                    for activity in activity_ids:
                        if activity.id != self.id and activity.state != 'done':
                            return False

            next_stage = self.env['mail.activity.stage'].search([('parent_stage_id', '=', self.stage_id.id)], limit=1)
            if self.rules:
                if safe_eval(self.rules, {'self': record}):
                    record.worklfow_stage_id = next_stage
                    record._create_stage_activities(next_stage)
                    return True
                raise ValidationError(_('The transitions rules are not valid for this activity'))
            else:
                record.worklfow_stage_id = next_stage
                record._create_stage_activities(next_stage)
                return True
        else:
            return True

    def _action_done(self, feedback=False, attachment_ids=None):
        self.set_next_stage()
        return super(MailActivity, self)._action_done(feedback=feedback, attachment_ids=attachment_ids)