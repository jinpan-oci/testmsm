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
    "name": "Mr Store custom browser",
    "summary": """
        This module contain the custom browser for Mr Store.
        """,
    "version": "17.0.1.9",
    "description": """
        This module contain the custom browser for Mr Store.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
    ],
    "data": [
        "views/browser_view.xml",
        "views/menu_item.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
