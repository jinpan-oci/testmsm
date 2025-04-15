//** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";

const { Component, useState, useEffect } = owl;

export class IframeCustomWidget extends Component {
    setup() {
        var self = this;
        console.log("Contexte:", this.props.context);

        this.state = useState({
            url: this.props.url || "",
            width: this.props.width || "",
            height: this.props.height || "",
            companyId: null,
            saleOrderId: null,
            saleOrderLineId: null,
        });
        if (this.props && this.props.context && this.props.context.company_id) {
            this.state.companyId = this.props.context.company_id;
        }
        if (this.props && this.props.context && this.props.context.order_id) {
            this.state.saleOrderId = this.props.context.order_id;
        }
        if (this.props && this.props.context && this.props.context.order_line_id) {
            this.state.saleOrderLineId = this.props.context.order_line_id;
        }
        if (this.props && this.props.context && this.props.context.line) {
            this.state.line = this.props.context.line;
        }

        useEffect(
            (el) => {
                if (!el) {
                    return;
                }

                if (self.state.width) {
                    el.style.width = self.state.width;
                } else {
                    el.style.width = '100%';
                }
                if (self.state.height) {
                    el.style.height = self.state.height;
                } else {
                    el.style.height = '550px';
                }
                window.addEventListener("message", self.handlePostMessage.bind(self));
                return () => {
                    window.removeEventListener("message", self.handlePostMessage.bind(self));
                };
            },
            () => [document.querySelector('.o_field_iframe_custom_widget')]
        );
        this.loadWizard();
    }

    async loadWizard() {
        const host = this.props.record.context.host;
        const subUrl = this.props.record.context.subUrl;
        const apitoolId = this.props.record.context.apiToolId;
        const usr = this.props.record.context.usr;
        const pwd = this.props.record.context.pwd;
        const callbacktoken = odoo.csrf_token;
        const companyId = this.props.record && this.props.record.context ? this.props.record.context.company_id : null;
        const saleOrderId = this.props.record && this.props.record.context ? this.props.record.context.order_id : null;
        const saleOrderLineId = this.props.record && this.props.record.context && this.props.record.context.order_line_id ? this.props.record.context.order_line_id : null;
        const baseUrl = this.props.record && this.props.record.context ? this.props.record.context.baseUrl : null;
        const line = this.props.record && this.props.record.context && this.props.record.context.line ? this.props.record.context.line : null;

        const callbackUrl = saleOrderLineId ? `${baseUrl}/hercule/update_product_and_sol/${companyId}/${saleOrderId}/${saleOrderLineId}` : `${baseUrl}/hercule/create_product_and_sol/${companyId}/${saleOrderId}`;
        const callback_js_post_message = 'line_saved';

        const dataObject = {
            external_tool: this.props.record.context.externalToolId,
            get_file: true,
            callback_url: callbackUrl,
            callback_js_post_message: callback_js_post_message,
            callback_token: callbacktoken
        };

        if (line !== null) {
            dataObject.line = line;
        }

        const data = JSON.stringify(dataObject);



        const urlEncodedDataPairs = [
            'usr=' + encodeURIComponent(usr),
            'pwd=' + encodeURIComponent(pwd),
            'apitoolId=' + encodeURIComponent(apitoolId),
            'data=' + encodeURIComponent(data),
        ];
        const urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

        try {
            const XHR = new XMLHttpRequest();

            XHR.onreadystatechange = () => {
                if (XHR.readyState === XMLHttpRequest.DONE) {
                    if (XHR.status === 200) {
                        const response = JSON.parse(XHR.responseText);
                        if (response.root && response.root.token) {
                            const iframeSrc = host + subUrl + 'sId=' + response.root.token;
                            this.state.url = iframeSrc; // Met à jour l'URL de l'iframe
                        } else {
                            console.error('Token non reçu');
                        }
                    } else {
                        console.error('Erreur de requête:', XHR.statusText);
                    }
                }
            };

            XHR.open('POST', host + '/rest/configuration/wizapi/load');
            XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            XHR.send(urlEncodedData);
        } catch (error) {
            console.error('Erreur lors de lenvoi de la requête:', error);
        }
    }

    handlePostMessage(event) {
        if (event.data === "line_saved") {
            const baseUrl = this.props.record.context.baseUrl;
            const saleOrderId = this.props.record.context.order_id;
            if (baseUrl && saleOrderId) {
                const saleOrderUrl = `${baseUrl}/web#id=${saleOrderId}&model=sale.order&view_type=form`;
                window.location.href = saleOrderUrl; // Redirige vers l'URL de la sale order
            } else {
                console.error('baseUrl ou saleOrderId est manquant');
            }
        }
    }

    get url() {
        return this.state.url || "";
    }
    get width() {
        return this.state.width || "";
    }
    get height() {
        return this.state.height || "";
    }
}

IframeCustomWidget.template = "IframeCustomWidget";
IframeCustomWidget.displayName = _lt("Iframe");
IframeCustomWidget.supportedTypes = ["text"];

export const iframecustomwidget = {
    component: IframeCustomWidget,
    extractProps: ({ attrs, options }) => {
        return {
            url: options.url,
            width: options.width || '100%',
            height: options.height || '550px',
        };
    },
}

registry.category("fields").add('iframe_custom_widget', iframecustomwidget);
