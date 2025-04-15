# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""


:copyright: (c) 2023 irokoo
:license: AGPLv3, see LICENSE for more details

"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval


class MailActivityStage(models.Model):
    _name = 'mail.activity.stage'
    _description = 'Mail Activity Stage'
    _order = 'sequence, id'

    def _get_model_selection(self):
        return [
            (model.model, model.name)
            for model in self.env['ir.model'].sudo().search(
                ['&', ('is_mail_thread', '=', True), ('transient', '=', False)])
        ]

    res_model = fields.Selection(selection=_get_model_selection, string="Model Stage",
        help='Specify a model stage.')
    name = fields.Char('Name')
    sequence = fields.Integer('Sequence', default=10)   
    is_start_stage = fields.Boolean('Is Start Stage')
    is_close_stage = fields.Boolean('Is Close Stage')
    activity_transition = fields.One2many('mail.activity.type', compute='_compute_activity_transition', string='Activity Transition')

    def _compute_activity_transition(self):
        for stage in self:
            stage.activity_transition = self.env['mail.activity.type'].search([('from_stage_id', '=', stage.id)], limit=1)


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    category = fields.Selection(selection_add=[('server', 'Server')])   
    from_stage_id = fields.Many2one('mail.activity.stage', 'From Stage', domain="[('res_model', '=', res_model)]")
    to_stage_id = fields.Many2one('mail.activity.stage', 'To Stage', domain="[('res_model', '=', res_model)]")
    rules = fields.Text(string='Python Rules')


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    stage_id = fields.Many2one('mail.activity.stage', 'Current Stage')
    rules = fields.Text('Rules', related='activity_type_id.rules')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(MailActivity, self).create(vals_list)
        for activity in res:
            activity.stage_id = activity.activity_type_id.from_stage_id
        return res

    def set_next_stage(self):
        self.ensure_one()
        model = self.env[self.res_model]  
        record = model.browse(self.res_id)
        if self.stage_id:
            next_stage = self.activity_type_id.to_stage_id
            if self.activity_type_id.triggered_next_type_id.from_stage_id == next_stage \
                    or next_stage.is_close_stage \
                    or self.activity_type_id.suggested_next_type_ids:
                if self.rules:
                    if safe_eval(self.rules, {'self': record}):
                        record.worklfow_stage_id = next_stage
                        return True
                    raise ValidationError(_('The transitions rules are not valid for this activity'))
                else:
                    record.worklfow_stage_id = next_stage
                    return True
            else:
                raise UserError(_('The next stage is not valid for this activity'))
        else:
            return True

    def _action_done(self, feedback=False, attachment_ids=None):
        if self.set_next_stage():
            res = super(MailActivity, self)._action_done(feedback=feedback, attachment_ids=attachment_ids)
        return res







