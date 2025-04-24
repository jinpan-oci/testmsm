/** @odoo-module **/

import { registry } from "@web/core/registry";
import { SaleOrderLineDescription } from "../components/sale_order_line_description/sale_order_line_description";

export const SaleOrderLineDescriptionWidget = {
    name: "SaleOrderLineDescriptionWidget",
    component: SaleOrderLineDescription,
};

registry.category("fields").add("sale_order_line_description_widget", SaleOrderLineDescriptionWidget);
