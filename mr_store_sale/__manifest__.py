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
    "name": "Mr Store Sale",
    "summary": """
        This module contain Mr Store Sale edits.
        """,
    "version": "17.0.5.2",
    "description": """
        This module contain Mr Store Sale edits.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "external_dependencies": {
        "python": [
            "beautifulsoup4",
        ]
    },
    "depends": [
        "base",
        "sale",
        "product",
        "mrp",
        "mrp_mps",
        "sign",
        "iframe_custom_widget",
    ],
    "data": [
        # data
        "data/mail_template.xml",
        # security
        "security/ir.model.access.csv",
        # wizards
        "wizards/sale_order_line_calculate.xml",
        "wizards/sale_order_line_change_description.xml",
        # views
        "views/sale_order_views.xml",
        "views/res_config_settings_views.xml",
        "views/account_tax_views.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
