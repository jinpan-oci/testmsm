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
    "name": "Base Sync Slave",
    "summary": """
        This module is the slave module of the base_sync_master module.
        """,
    "version": "17.0.1.8",
    "description": """
        This module is the slave module of the base_sync_master module.
        It allows to synchronize the data of the master database with the slave database.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "base_import",
        "product",
        "stock",
    ],
    "data": [
        # data
        "data/ir_cron.xml",
        # security
        "security/ir.model.access.csv",
        # report
        # views
        "views/base_sync_views.xml",
        "views/base_sync_line_views.xml",
        "views/base_sync_master_id_config_views.xml",
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
