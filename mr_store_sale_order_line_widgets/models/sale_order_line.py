# -*- coding: utf-8 -*-
from odoo import models, fields, api
from bs4 import BeautifulSoup

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sale_order_line_menu = fields.Char(string="Menu")
    sale_order_line_short_description = fields.Char(string="Short Description", compute="_compute_sale_order_line_short_description", store=True)

    @api.depends('name', 'description_html')
    def _compute_sale_order_line_short_description(self):
        for rec in self:
            if rec.description_html:
                rec.sale_order_line_short_description = self.first_text_line(self.html_to_text(rec.description_html))
            else:
                rec.sale_order_line_short_description = self.first_text_line(rec.name)

    def html_to_text(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text("\n")

    def first_text_line(self, text):
        if not text:
            return ""
        return text.split("\n")[0]
