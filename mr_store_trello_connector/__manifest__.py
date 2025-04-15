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
    "name": "Mr Store - Trello Connector",
    "summary": """
        This module enables Odoo to synchronize master catalog with odoo's members'.
        """,
    "version": "17.0.4.3",
    "description": """
        This module enables Odoo to synchronize master catalog with odoo's members'.
        """,
    "author": "ama@irokoo",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "sale",
        "project",
        "sale_project",
        "mr_store_settings",
        "mr_store_installation_page",
        "mr_store_report_folder",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "views/trello_sync.xml",
        "views/project_task_type_view.xml",
        "views/sale_order_view.xml",
        "views/project_task_view.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_view.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
