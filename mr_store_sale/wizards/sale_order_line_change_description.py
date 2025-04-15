from bs4 import BeautifulSoup
from odoo import fields, models


class SaleOrderLineChangeDescription(models.TransientModel):
    _name = "sale.order.line.change.description.wizard"
    _description = "Change Description Wizard"

    line_id = fields.Many2one("sale.order.line", string="Order line")
    presentation_before = fields.Html(string="Presentation Before")
    # description_text = fields.Char(string="Description Text")
    description_html = fields.Html(string="Description Html")
    presentation_after = fields.Html(string="Presentation After")

    def html_to_text(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text("\n")

    def text_to_html(self, text):
        return text.replace("\n", "<br/>").replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;").replace("\r", "")

    def default_get(self, fields):
        rec = super().default_get(fields)
        active_id = self.env.context.get("active_id", False)
        sol = self.env["sale.order.line"].browse(active_id)
        desc = ""
        if sol.description_html:
            desc = sol.description_html
        elif sol.description_text:
            desc = self.text_to_html(sol.description_text)
        elif sol.name:
            desc = self.text_to_html(sol.name)

        rec.update(
            {
                "line_id": active_id,
                "description_html": desc,
                # "description_text": sol.name,
                "presentation_before": (sol.presentation_before if sol.presentation_before else sol.product_id.presentation_before),
                "presentation_after": (sol.presentation_after if sol.presentation_after else sol.product_id.presentation_after),
            }
        )
        return rec

    def change_description(self):
        self.ensure_one()
        self.line_id.with_context(no_update=True).write(
            {
                "description_html": self.description_html,
                "description_text": self.html_to_text(self.description_html),
                "name": self.html_to_text(self.description_html),
                "presentation_before": self.presentation_before,
                "presentation_after": self.presentation_after,
            }
        )
        return {"type": "ir.actions.act_window_close"}
