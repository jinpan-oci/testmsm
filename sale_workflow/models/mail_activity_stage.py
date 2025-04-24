# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""


:copyright: (c) 2023 irokoo
:license: AGPLv3, see LICENSE for more details

"""
from odoo import api, fields, models, _


class MailActivityStage(models.Model):
    _name = 'mail.activity.stage'
    _description = 'Mail Activity Stage'
    _order = 'sequence asc'
    _sql_constraints = [
        ('unique_parent_stage_id', 'unique(parent_stage_id)', 'A stage with the same parent already exist.')
    ]

    def _get_model_selection(self):
        return [
            (model.model, model.name)
            for model in self.env['ir.model'].sudo().search(
                ['&', ('is_mail_thread', '=', True), ('transient', '=', False)])
        ]

    res_model = fields.Selection(selection=_get_model_selection, string="Model Stage",
        help='Specify a model stage.')
    name = fields.Char('Name')
    sequence = fields.Integer('Sequence', compute='_compute_sequence', store=True, recursive=True)
    parent_stage_id = fields.Many2one('mail.activity.stage', 'Parent Stage', domain="[('res_model', '=', res_model)]")
    activity_type_ids = fields.One2many('mail.activity.type', compute='_compute_activity_type_ids', string='Activity Types')
    wait_for_all_activities = fields.Boolean('Wait for all activities', help='Wait for all activities to be done before moving to the next stage', default=True)

    def _compute_activity_type_ids(self):
        for stage in self:
            stage.activity_type_ids = self.env['mail.activity.type'].search([('stage_id', '=', stage.id)])

    @api.depends('parent_stage_id', 'parent_stage_id.sequence')
    def _compute_sequence(self):
        for stage in self:
            if stage.parent_stage_id:
                stage.sequence = stage.parent_stage_id.sequence + 1
            else:
                model_selection = self._get_model_selection()
                for model in model_selection:
                    if model[0] == stage.res_model:
                        stage.sequence = model_selection.index(model) * 100
                        break

    def cron_job(self):
        for record in self.search([('parent_stage_id', '=', False)]):
            if record.res_model:
                for rec in self.env[record.res_model].search([('create_activities', '=', True)]):
                    rec._create_stage_activities(rec.worklfow_stage_id)
                    rec.create_activities = False
        return True

    def run_cron(self):
        cron = self.env['ir.cron'].sudo().search([('active', '=', 'False'), ('model_id', '=', 'sale_workflow.model_mail_activity_stage'), ('code', '=', 'model.cron_job()')])
        cron.write({
            'active': True,
            'numcall': 1,
        })





