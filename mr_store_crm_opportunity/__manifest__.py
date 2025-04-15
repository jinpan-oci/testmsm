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
    "name": "Mr Store CRM Opportunity",
    "summary": """
        This module contain all Mr Store CRM/Opportunity edits.
        """,
    "version": "17.0.2.0",
    "description": """
        This module contain all Mr Store CRM/Opportunity edits.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "calendar",
        "sale",
        "sale_crm",
    ],
    "data": [
        "views/calendar_event_view.xml",
        "views/crm_lead_view.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
