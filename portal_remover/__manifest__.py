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
    "name": "Portal Remover",
    "summary": """
        This adds a boolean to deactivate portal access.
        """,
    "version": "17.0.0.0",
    "description": """
        This adds a boolean to deactivate portal access.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": [r"static\description\icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "base_setup",
    ],
    "data": [
        # security
        # wizards
        # views
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
