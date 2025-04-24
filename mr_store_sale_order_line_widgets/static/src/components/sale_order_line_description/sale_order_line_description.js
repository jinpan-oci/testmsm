/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class SaleOrderLineDescription extends Component {
    static template = "sale_order_line_description.SaleOrderLineDescriptionTemplate";
    static props = {
        record: Object,
        name: String,
        readonly: { type: Boolean, optional: true },
    };

    setup() {
        super.setup();
        this.state = useState({
            expanded: false,
        });
        this.record = this.props.record.data;
    }

    get displayedDescription() {
        if (this.state.expanded || !this.record.name) {
            return this.record.name;
        } else {
            return this.record.sale_order_line_short_description;
        }
    }

    toggleDescription() {
        this.state.expanded = !this.state.expanded;
    }
}
