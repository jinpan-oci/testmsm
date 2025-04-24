/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class SaleOrderLineMenu extends Component {
    static template = "sale_order_line_menu.SaleOrderLineMenuTemplate";
    static props = {
        record: Object,
        name: String,
        readonly: { type: Boolean, optional: true },
    };

    setup() {
        super.setup();
        this.props = useState(this.props);
        this.record = this.props.record.data;
        this.parent = this.props.record._parentRecord.data

        this.orm = useService("orm");
        this.action = useService("action");

        this.companyId = this.record.company_id[0];
        this.saleOrderId = this.record.order_id[0];
        this.saleOrderLineId = this.record.id;
    }

    async fetchUpdatedLine(fields_to_read = []) {
        try{
            const updatedLine = await this.orm.read(
                "sale.order.line",
                [this.saleOrderLineId],
                fields_to_read
            );
            Object.assign(this.record, updatedLine[0]);

        } catch (error){
            console.error("Failed to fetch updated record data:", error);
        }
    }

    async onClickDescription() {
        try {
            await this.action.doAction("mr_store_sale.sale_order_line_change_description_action", {
                additionalContext: {
                    active_model: "sale.order.line",
                    active_id: this.saleOrderLineId, 
                    default_line_id: this.saleOrderLineId, 
                },
                onClose: () => {
                    this.fetchUpdatedLine(['name', 'sale_order_line_short_description', 'description_html']);
                }
            });
        } catch (error) {
            console.error("Failed to execute action:", error);
        }
    }

    get showClickEStory() {
        return this.record.full_code || false;
    }
    async onClickEStory() {
        const context = {
            order_id: this.saleOrderId,
            line_id: this.saleOrderLineId,
            allowed_company_ids: [this.companyId],
        };
        try {
            const action = await this.orm.call(
                "sale.order.line",
                "action_edit_from_hp5",
                [[this.saleOrderLineId]],
                {
                    context
                }
            );
            await this.action.doAction(action);
        } catch (error) {
            console.error("Failed to execute action:", error);
        }
    }

    get showClickCalculate() {
        var bool = this.record.use_update_price_line_wizard 
        bool = bool && this.record.product_type == 'product' 
        bool = bool && !this.parent.locked
        return bool || false;
    }
    async onClickCalculate() {
        try {
            await this.action.doAction("mr_store_sale.sale_order_line_service_update_action", {
                additionalContext: {
                    active_model: "sale.order.line",
                    active_id: this.saleOrderLineId, 
                    default_line_id: this.saleOrderLineId, 
                },
                onClose: async () => {
                    // await this.fetchUpdatedLine(['price_unit', 'estimated_time', 'price_subtotal']);
                    await this.action.doAction({'type': 'ir.actions.client', 'tag': 'soft_reload'})
                }
            });
        } catch (error) {
            console.error("Failed to execute action:", error);
        }
    }

}
