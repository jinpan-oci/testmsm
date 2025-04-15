# Copyright 2024 irokoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale order alternatives",
    "summary": "Keep track of alternatives quotations",
    "version": "17.0.2.0.1",
    "category": "Sale Management",
    "author": "irokoo",
    "website": "https://www.irokoo.fr",
    "license": "AGPL-3",
    "depends": ["sale_management"],
    "data": [
        # security
        "security/ir.model.access.csv",
        "security/user_groups.xml",
        # report
        "report/sale_order_portal_views.xml",
        # views
        "view/sale_order.xml",
    ],
    "installable": True,
    "application": True,
}
