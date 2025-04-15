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
    "name": "Mr Store Report Folder",
    "summary": """
        This module contain Mr Store report folder.
        """,
    "version": "17.0.3.14",
    "description": """
        This module contain Mr Store report folder.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "external_dependencies": {
        "python": [
            "oauthlib==3.2.2",
            "requests-oauthlib==1.3.1",
            "pdf2image==1.17.0",
            "poppler-utils==0.1.0",
        ],
        "bin": [],
    },
    "depends": [
        "base",
        "sale",
        "project",
        "mr_store_installation_page",
        "mr_store_contacts",
        "mr_store_settings",
        "mr_store_sale",
        "iframe_custom_widget",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/report_paperformat_data_mr_store.xml",
        "report/ir_actions_report.xml",
        "views/folder_template.xml",
        "views/internal_layout_mr_store.xml",
        "views/sale_order_view.xml",
        "views/res_config_settings_view.xml",
        "views/ir_attachment_views.xml",
        "wizard/attachment_add_view.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
