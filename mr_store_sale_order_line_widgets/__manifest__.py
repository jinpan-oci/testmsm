# -*- coding: utf-8 -*-
{
    'name': "mr_store_sale_order_line_widgets",
    'description': "Mr Store Sale Order Line Widgets",
    'category': 'Customizations/Settings',
    'version': "17.0.0.0.2",
    'author': "IROKOO, Fabien DESPREZ",
    'license': 'Other proprietary',
    'website': 'https://irokoo.fr',
    'sequence': 0,
    'auto_install': False,
    'installable': True,
    'application': False,

    'depends': [
        'base',
        'sale',
        'mr_store_sale',
        'iframe_custom_widget',
    ],
    'data': [
        "views/sale_order_views.xml",
    ],
    'images': [
        'static/description/icon.png',
    ],
    'assets': {
        'web.assets_backend': [
            '/mr_store_sale_order_line_widgets/static/src/components/**/*.js',
            '/mr_store_sale_order_line_widgets/static/src/components/**/*.css',
            '/mr_store_sale_order_line_widgets/static/src/components/**/*.xml',
            '/mr_store_sale_order_line_widgets/static/src/js/sale_order_line_menu_widget.js',
            '/mr_store_sale_order_line_widgets/static/src/js/sale_order_line_description_widget.js',
        ],
    }
}
