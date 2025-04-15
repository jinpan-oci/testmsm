#################################################################################
# Author      : irokoo
# Copyright(c): 2023 - irokoo
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#
#################################################################################

{
    "name": "Mr Store report",
    "summary": """
        This module contain all Mr Store custom reports.
        """,
    "version": "17.0.3.12",
    "description": """
        This module contain all Mr Store custom reports.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "sale",
        "sale_management",
        "account",
        "web",
        "product",
        "purchase",
        "mr_store_report_folder",
        "portal_remover",
        "mr_store_sale",
        "iframe_custom_widget",
    ],
    "data": [
        # data
        "data/report_paperformat_data.xml",
        # security
        # report invoice
        "report/invoice/account_document_tax_totals.xml",
        "report/invoice/external_layout.xml",
        # layout invoice mail format enveloppe fenetre
        "report/invoice/external_layout_mail.xml",
        "report/invoice/ir_actions_report.xml",
        "report/invoice/report_invoice.xml",
        # report invoice mail format enveloppe fenetre
        "report/invoice/invoice_mail.xml",
        "report/invoice/tax_groups_totals.xml",
        # report purchase order
        "report/purchase_order/external_layout.xml",
        "report/purchase_order/ir_actions_report.xml",
        "report/purchase_order/report_purchase_order.xml",
        # report sale order
        "report/sale_order/document_tax_totals_template.xml",
        "report/sale_order/external_layout.xml",
        "report/sale_order/ir_actions_report.xml",
        "report/sale_order/report_sale_order.xml",
        # report sale order alternative
        "report/sale_order_alternative/document_tax_totals_template.xml",
        "report/sale_order_alternative/external_layout.xml",
        "report/sale_order_alternative/ir_actions_report.xml",
        "report/sale_order_alternative/report_sale_order.xml",
        # report sale order light
        "report/sale_order_light/document_tax_totals_template.xml",
        "report/sale_order_light/external_layout.xml",
        "report/sale_order_light/ir_actions_report.xml",
        "report/sale_order_light/report_sale_order.xml",
        # views
        "views/account_move_views.xml",
        "views/product_template_view.xml",
        "views/product_views.xml",
        "views/sale_order_portal_views.xml",
        "views/sale_order_views.xml",
        # wizard
        "wizard/base_document_layout_views_mr_store.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
