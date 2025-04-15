# Copyright 2024 irokoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html
from odoo import Command, api, fields, models


class SoAlternativeGroup(models.Model):
    _name = "so.alternative.group"
    _description = "Technical model to group Quotations"

    order_ids = fields.One2many("sale.order", "sale_order_group_id")

    def write(self, vals):
        res = super().write(vals)
        # when len(POs) == 1, only linking PO to itself at this point => self implode (delete) group
        self.filtered(lambda g: len(g.order_ids) <= 1).unlink()
        return res


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_order_group_id = fields.Many2one("so.alternative.group")
    alternative_so_ids = fields.One2many(
        "sale.order",
        related="sale_order_group_id.order_ids",
        readonly=False,
        domain="[('id', '!=', id), ('state', 'in', ['draft', 'sent'])]",
        string="Alternative SOs",
        check_company=True,
        help="Other potential quotes for customer",
    )
    has_alternatives = fields.Boolean(
        "Has Alternatives",
        compute="_compute_has_alternatives",
        help="Whether or not this quote order is linked to another quote order as an alternative.",
    )

    alternatives_count = fields.Integer("Alternatives", compute="_compute_alternatives_count")

    @api.depends("alternative_so_ids")
    def _compute_alternatives_count(self):
        for so in self:
            so.alternatives_count = len(so.alternative_so_ids)

    @api.depends("sale_order_group_id")
    def _compute_has_alternatives(self):
        self.has_alternatives = False
        self.filtered(lambda so: so.sale_order_group_id).has_alternatives = True

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        if self.env.context.get("origin_so_id"):
            # so created as an alt to another SO:
            origin_so_id = self.env["sale.order"].browse(self.env.context.get("origin_so_id"))
            if origin_so_id.sale_order_group_id:
                origin_so_id.sale_order_group_id.order_ids |= orders
            else:
                self.env["so.alternative.group"].create({"order_ids": [Command.set(origin_so_id.ids + orders.ids)]})
        return orders

    def action_create_alternative(self):
        alt_so = self.with_context(origin_so_id=self.id).copy()
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": alt_so.id,
            "context": {
                "active_id": alt_so.id,
            },
        }

    def action_view_alternatives(self):
        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "domain": [("sale_order_group_id", "=", self.sale_order_group_id.id)],
            "context": {
                "create": False,
            },
        }

    def _action_confirm(self):
        res = super()._action_confirm()
        for record in self:
            if record.has_alternatives:
                for alt_so in record.alternative_so_ids:
                    if alt_so.id != record.id and alt_so.state != "cancel":
                        alt_so.action_cancel()
        return res

    def copy_inherit(self, default=None):
        res = super().copy(default)
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": res.id,
            "context": {
                "active_id": res.id,
            },
        }
