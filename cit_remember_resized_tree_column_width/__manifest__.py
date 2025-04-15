##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    "name": "Remember Resized Tree Column Width",
    "version": "17.0.0.1",
    "license": "OPL-1",
    "summary": """
        Resize Column Width, Remember the tree view column's width each and every session.""",
    "category": "Sales/Sales",
    "sequence": 1,
    "description": "This module is used to Auto save when the user resizes the tree view column's widths or one2many fields column's width.",
    "author": "Caret IT Solutions Pvt. Ltd.",
    "website": "https://www.caretit.com",
    "depends": ["web", "account", "sale_management"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "cit_remember_resized_tree_column_width/static/src/js/list_renderer_account.js",
            "cit_remember_resized_tree_column_width/static/src/js/list_renderer.js",
            "cit_remember_resized_tree_column_width/static/src/js/section_list.js",
            "cit_remember_resized_tree_column_width/static/src/scss/main.scss",
        ],
    },
    "images": ["static/description/banner.gif"],
    "price": 19.00,
    "currency": "EUR",
}
