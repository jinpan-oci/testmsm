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
    "name": "Mr Store Sale Order Type",
    "summary": """
        This module contain Mr Store Sale type quotation.
        """,
    "version": "17.0.0.0",
    "description": """
        This module contain Mr Store Sale type quotation.
        """,
    "author": "irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "sale",
        "account",
        "mr_store_report",
    ],
    "data": [
        # security
        # wizards
        # views
        "views/sale_order_type_views.xml",
        "views/account_move_type_views.xml",
        # data
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
