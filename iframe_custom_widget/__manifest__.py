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
    "name": "Iframe Widget | Iframe",
    "summary": """
        This module enables Odoo to acces hercule configurator'.
        """,
    "version": "17.0.8.3",
    "description": """
        This module enables Odoo to acces hercule configurator'.
        """,
    "author": "ama@irokoo",
    "maintainer": "",
    "license": "LGPL-3",
    "website": "",
    "images": ["images/iframe_custom_widget.png"],
    "category": "Extra Tools",
    "external_dependencies": {
        "python": [
            "hashlib",
        ],
        "bin": [],
    },
    "depends": [
        "base",
        "sale",
        "web",
    ],
    "data": [
        # security
        "security/ir.model.access.csv",
        # views
        "views/hercule_label_views.xml",
        "views/hercule_product_views.xml",
        "views/hercule_title_views.xml",
        "views/hercule_category_views.xml",
        "views/res_config_settings_view.xml",
        "views/sale_order_views.xml",
        # menuitem
        "views/menuitem.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/iframe_custom_widget/static/src/js/*.js",
            "/iframe_custom_widget/static/src/css/*.css",
            "/iframe_custom_widget/static/src/xml/*.xml",
        ],
    },
    "installable": True,
    "application": True,
    "price": 0,
    "currency": "EUR",
}
