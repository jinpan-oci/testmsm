from odoo import fields, models, api
from odoo.exceptions import UserError

INVOICE_STATUS = [
    ("upselling", "Upselling Opportunity"),
    ("invoiced", "Fully Invoiced"),
    ("to invoice", "To Invoice"),
    ("no", "Nothing to Invoice"),
]


class SaleOrder(models.Model):
    _inherit = "sale.order"

    P = fields.Char(string="P - Installer Number", help="P")
    H = fields.Char(string="H - Hours Number", help="H")
    AP = fields.Char(string="AP - Forwarding Installer Number", help="AP")
    AH = fields.Char(string="AH - Forwarding Time", help="AH")
    L = fields.Char(string="L - Zip Code or Place Name", help="L")

    is_planned = fields.Boolean(string="Is Planned", default=False, compute="_compute_is_planned")

    def action_planify(self):
        self.ensure_one()
        if self.tasks_ids:
            self.env["trello.sync"].push_one(self)
            return {
                "type": "ir.actions.act_url",
                # 'target': 'self',
                "url": self.env["trello.sync"].get_actual_board().url,
            }
        else:
            raise UserError("Unable to planify a sale order without associated Service/Task and Trello card id")

    def action_cancel(self):
        self.ensure_one()
        if self.is_planned:
            for task in self.tasks_ids:
                if task.trello_idcardsource:
                    client = self.env["trello.sync"].get_instance()
                    card_to_delete = client.get_card(str(task.trello_idcardsource))
                    card_to_delete.delete()
                    self.is_planned = False
                    task.trello_idcardsource = ""
        res = super().action_cancel()
        return res

    @api.depends("tasks_ids", "tasks_ids.trello_idcardsource")
    def _compute_is_planned(self):
        for order in self:
            is_planned = False
            if order.tasks_ids:
                for task in order.tasks_ids:
                    if task.trello_idcardsource:
                        is_planned = True
                        break
            order.is_planned = is_planned
