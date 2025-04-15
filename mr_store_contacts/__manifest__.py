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
    "name": "Mr Store Contacts",
    "summary": """
        This module add more contacts informations for Mr Store delivery.
        """,
    "version": "17.0.1.9",
    "description": """
        This module add more contacts informations for Mr Store delivery.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "crm",
        "sale",
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/crm_lead_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
