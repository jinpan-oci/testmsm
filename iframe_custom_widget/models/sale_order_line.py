from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    full_code = fields.Char(string="Full Code")
    hercule_line = fields.Char(string="Line", store=True)
    description_html = fields.Html(string="Description Html", compute="_compute_description", store=True)
    description_text = fields.Text(string="Description Text", compute="_compute_description", store=True)

    def action_add_from_hp5(self):
        form_view_id = self.env.ref("iframe_custom_widget.sale_product_h5_form_view").id
        order_id = self.env["sale.order"].browse(self._context.get("order_id"))
        company_id = order_id.company_id
        return {
            "type": "ir.actions.act_window",
            "name": _("Products"),
            "res_model": "product.product",
            "views": [(form_view_id, "form")],
            "domain": [("id", "=", 1)],
            "context": {
                "order_id": order_id.id,
                "company_id": company_id.id,
                "host": self.env["ir.config_parameter"].with_company(self.company_id.id).sudo().get_param("iframe_host"),
                "subUrl": self.env["ir.config_parameter"].with_company(self.company_id.id).sudo().get_param("iframe_sub_url"),
                "apiToolId": self.env["ir.config_parameter"].with_company(self.company_id.id).sudo().get_param("iframe_api_tool_id"),
                "usr": self.env["ir.config_parameter"].with_company(self.company_id.id).sudo().get_param("iframe_usr"),
                "pwd": self.env["ir.config_parameter"].with_company(self.company_id.id).sudo().get_param("iframe_md5_pwd"),
                "externalToolId": self.env["ir.config_parameter"].with_company(self.company_id.id).sudo().get_param("iframe_external_tool_id"),
                "baseUrl": self.env["ir.config_parameter"].with_company(self.company_id.id).sudo().get_param("web.base.url"),
            },
            "help": _(
                """<p class="o_view_nocontent_smiling_face">
                Create a new product
            </p><p>
                You must define a product for everything you sell or purchase,
                whether it's a storable product, a consumable or a service.
            </p>"""
            ),
        }

    def action_edit_from_hp5(self):
        res = self.action_add_from_hp5()
        line_id = self.env["sale.order.line"].browse(self._context.get("line_id"))
        res["context"]["order_line_id"] = line_id.id
        res["context"]["line"] = eval(line_id.hercule_line)
        return res

    def action_open_configurator(self):
        return {
            "type": "ir.actions.act_url",
            # 'target': 'self',
            "url": "https://monsieurstore-catalogue.artefacto.eu/webapp/",
        }

    def text_to_html(self, text):
        return text.replace("\n", "<br/>").replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;").replace("\r", "")

    # @api.onchange("name")
    # def onchange_name(self):
    #     for record in self:
    #         if record.name:
    #             if record.display_type not in ["line_section", "line_note"]:
    #                 record.name = record.name[:97] + "..." if len(record.name) > 100 else record.name

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            if rec.name:
                if not rec.full_code:
                    rec.description_text = rec.name
                    rec.description_html = rec.text_to_html(rec.name)
                # if rec.display_type not in ["line_section", "line_note"]:
                #     rec.name = rec.name[:97] + "..." if len(rec.name) > 100 else rec.name
        return res

    @api.depends("name")
    def _compute_description(self):
        for record in self:
            if record.name != record.description_text and not record.full_code:
                record.description_text = record.name
                record.description_html = record.text_to_html(record.name)
            else:
                record.description_text = record.description_text or ""
                record.description_html = record.description_html or ""
