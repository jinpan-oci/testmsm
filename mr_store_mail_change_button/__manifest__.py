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
    "name": "Mr Store Mail Change Button",
    "summary": """
        This module contain Mr Store mail change button.
        """,
    "version": "17.0.0.1",
    "description": """
        This module contain Mr Store mail change button.
        It change the "Sign & Pay Quotation" button to "View Quotation" in mails sent.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["static/description/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "sale",
        "account"
    ],
    "data": [
        "data/mail_layout.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
