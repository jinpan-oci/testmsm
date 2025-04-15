from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError
from datetime import date,datetime,timedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"

    worklfow_stage_id = fields.Many2one('mail.activity.stage', 'Current Stage', readonly=True, tracking=True) #to do : add to mixins

    @api.model_create_multi
    def create(self, vals_list):
        records = super(SaleOrder, self).create(vals_list)
        for record in records:
            record._init_workflow()
        return records

    def _init_workflow(self):
        for order in self:
            if order.commitment_date:
                deadline = fields.Date.from_string(order.commitment_date) - timedelta(days=3)
            else:
                deadline = fields.Date.today()
            first_stage = self.env['mail.activity.stage'].search([('is_start_stage', '=', True), ('res_model','=','sale.order')], limit=1)
            order.worklfow_stage_id = first_stage
            if first_stage:
                activity_type = self.env['mail.activity.type'].search([('from_stage_id', '=', first_stage.id), ('res_model','=','sale.order')], limit=1)
                if activity_type:
                    self.env['mail.activity'].create({
                            'activity_type_id': activity_type.id,
                            'date_deadline': deadline,
                            'user_id': self.env.uid,
                            'res_id': order.id,
                            'res_model_id': self.env['ir.model']._get('sale.order').id,
                        })
        return True
