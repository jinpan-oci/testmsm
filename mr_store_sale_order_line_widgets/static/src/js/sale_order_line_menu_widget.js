/** @odoo-module **/

import { registry } from "@web/core/registry";
import { SaleOrderLineMenu } from "../components/sale_order_line_menu/sale_order_line_menu";

export const SaleOrderLineMenuWidget = {
    name: "SaleOrderLineMenuWidget",
    component: SaleOrderLineMenu,
};

registry.category("fields").add("sale_order_line_menu_widget", SaleOrderLineMenuWidget);
