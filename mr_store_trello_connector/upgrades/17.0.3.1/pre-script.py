from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    orders = env["sale.order"].search([("state", "=", "plan")])
    for order in orders:
        order.state = "sale"
