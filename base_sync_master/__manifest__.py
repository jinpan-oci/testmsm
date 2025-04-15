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
    "name": "Base Sync Master",
    "summary": """
        This module let you sync multiple base with a master base. Master.
        """,
    "version": "17.0.2.0",
    "description": """
        This module let you sync multiple base with a master base.
        This one is the master module.
        """,
    "author": "gab@irokoo.fr",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/icon.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "base_automation",
        "product",
        "stock",
        "contacts",
    ],
    "data": [
        # data
        "data/ir_sequence_data.xml",
        # report
        # views
        "views/base_sync_line_views.xml",
        "views/base_sync_slaves_config.xml",
        "views/base_sync_template_config.xml",
        "views/base_sync_views.xml",
        "views/product_category_views.xml",
        "views/product_tag_views.xml",
        "views/product_template_attribute_line_views.xml",
        # security
        "security/ir.model.access.csv",
        # wizard
    ],
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
