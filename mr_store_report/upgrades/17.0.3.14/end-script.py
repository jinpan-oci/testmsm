from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Adapt order_report_type with existing pu_position values"""
    env = api.Environment(cr, SUPERUSER_ID, {})

    sale_orders = env["sale.order"].search([("pu_position_selection", "!=", None)])

    # match old value and set corresponding new value
    for sale_order in sale_orders:
        match sale_order.pu_position_selection:
            case "with_pu_top":
                sale_order.order_report_type = "quote_sale_order_with_pu_top"
            case "with_pu_bot":
                sale_order.order_report_type = "quote_sale_order_with_pu_bot"
            case "without_pu":
                sale_order.order_report_type = "quote_sale_order_without_pu"
            case _:
                sale_order.order_report_type = "quote_sale_order_with_pu_top"

    env = api.Environment(cr, SUPERUSER_ID, {})

    account_moves = env["account.move"].search([])

    for account_move in account_moves:
        # force new compute to recompute with new value
        if account_move.pu_position_selection:
            account_move._compute_pu_position_selection()
