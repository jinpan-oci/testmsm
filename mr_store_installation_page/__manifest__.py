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
    "name": "Mr Store Report Folder Installation Page",
    "summary": """
        This module contain Mr Store report folder installation page.
        """,
    "version": "17.0.3.5",
    "description": """
        This module contain Mr Store report folder installation page.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["static/description/icon.png"],
    "category": "Extra Tools",
    # "external_dependencies": {
    #     "python": [
    #     ],
    #     "bin": [],
    # },
    "depends": [
        "base",
        "sale",
    ],
    "data": [
        # security
        "security/ir.model.access.csv",
        # views
        "views/base_installation_settings.xml",
        "views/sale_order_views.xml",
        "views/transaction_installation_views.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
