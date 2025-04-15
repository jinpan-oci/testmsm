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
    "name": "Module Updater",
    "summary": """
        This module let you update a module list on slaves servers.
        """,
    "version": "17.0.1.9",
    "description": """
        This module let you update a module list on slaves servers.
        It is the slave and master at the same time.
        """,
    "author": "irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "category": "Extra Tools",
    "depends": [
        "base",
    ],
    "data": [
        # data
        # report
        # security
        "security/ir.model.access.csv",
        "security/user_groups.xml",
        # views qweb
        # views
        "views/module_install_tag_views.xml",
        "views/module_update_tag_views.xml",
        "views/module_updater_line_views.xml",
        "views/module_updater_views.xml",
        # menuitem
        "views/menuitems.xml",
        # wizard
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
