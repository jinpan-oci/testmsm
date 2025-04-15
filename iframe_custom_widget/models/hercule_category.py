from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class Hp5CategMatrix(models.Model):
    _name = "hercule.category"
    _description = "Hercule Category Matrix"
    _order = "sequence desc"

    full_code = fields.Char(string="Full Code")
    categ_id = fields.Many2one("product.category", string="Category")
    sequence = fields.Integer(string="Sequence", compute="_compute_sequence", store=True)

    @api.depends("full_code")
    def _compute_sequence(self):
        for record in self:
            if record.full_code:
                record.sequence = ord(record.full_code[0]) * 100000
                if len(record.full_code) > 3:
                    record.sequence += ord(record.full_code[3]) * 10000
                    if len(record.full_code) > 6:
                        record.sequence += ord(record.full_code[6]) * 1000
                        if len(record.full_code) > 9:
                            record.sequence += ord(record.full_code[9]) * 100
                            if len(record.full_code) > 12:
                                record.sequence += ord(record.full_code[12]) * 10
                                if len(record.full_code) > 15:
                                    record.sequence += ord(record.full_code[15])
            else:
                record.sequence = 0

    def action_repare_mes_betises(self):
        # for order_line in self.env["sale.order.line"].search([]):
        #     if order_line.name[-3:] == "...":
        #         if order_line.description_text and not order_line.description_text[-3:] == "...":
        #             order_line.name = order_line.description_text
        #         else:
        #             _logger.error("Order line %s has a name ending with '...' but no description_text", order_line.id)

        for order in self.env["sale.order"].search([]):
            if order.state == "cancel" or order.state == "done":
                continue
            if order.order_line:
                to_lock = False
                if order.locked:
                    to_lock = True
                    order.locked = False
                for order_line in order.order_line:
                    if order_line.name[-3:] == "...":
                        if order_line.description_text and not order_line.description_text[-3:] == "...":
                            order_line.name = order_line.description_text
                        else:
                            _logger.error(f"Order line {order_line.id!r} in order {order.id!r} has a name ending with '...' and no description_text")
                if to_lock:
                    order.locked = True
