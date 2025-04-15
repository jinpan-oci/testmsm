from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    orders = env["sale.order"].search([("state", "=", "sale"), ("tasks_ids", "!=", False)])

    for order in orders:
        for task in order.tasks_ids:
            if task.trello_idcardsource:
                order.is_planned = True
                break
