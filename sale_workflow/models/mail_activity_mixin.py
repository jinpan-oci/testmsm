from odoo import _, api, fields, models

class MailActivityMixin(models.AbstractModel):
    _inherit = 'mail.activity.mixin'
    _description = 'Mail Activity Mixin'

    worklfow_stage_id = fields.Many2one('mail.activity.stage', 'Current Stage', readonly=True, tracking=True)
    create_activities = fields.Boolean('Create Activities', default=False)

    def _create_stage_activities(self, stage):
        for record in self:
            if not stage:
                stage = record.worklfow_stage_id
            if stage:
                if stage.activity_type_ids:
                    for activity_type in stage.activity_type_ids:
                        user_id = activity_type.default_user_id or self.env['res.users'].search([('id', '=', record.user_id.id)], limit=1) or self.env.user
                        self.env['mail.activity'].create({
                            'activity_type_id': activity_type.id,
                            'date_deadline': fields.Date.today(),
                            'user_id': user_id.id,
                            'res_id': record.id,
                            'res_model_id': self.env['ir.model']._get(record._name).id,
                        })
        return True

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            first_stage = self.env['mail.activity.stage'].search([('parent_stage_id', '=', False), ('res_model','=',self._name)], limit=1)
            if first_stage:
                rec.worklfow_stage_id = first_stage
                rec.create_activities = True
                first_stage.run_cron()
        return res