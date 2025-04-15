import io
import base64

from odoo import models, _
from odoo.tools import pdf
from PyPDF2 import PdfFileWriter


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        result = super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids=res_ids)
        if self._get_report(report_ref).report_name not in [
            "mr_store_report.ms_report_saleorder",
            "mr_store_report.ms_report_saleorder_alternative",
        ]:
            return result

        orders = self.env["sale.order"].browse(res_ids)

        for order in orders:
            initial_stream = result[order.id]["stream"]
            if initial_stream:
                order_template = order.sale_order_template_id
                header_record = order_template if order_template.sale_header else order.company_id
                footer_record = order_template if order_template.sale_footer else order.company_id
                has_header = bool(header_record.sale_header)
                has_footer = bool(footer_record.sale_footer)
                included_product_docs = self.env["product.document"]
                doc_line_id_mapping = {}
                for line in order.order_line:
                    product_product_docs = line.product_id.product_document_ids
                    product_template_docs = line.product_template_id.product_document_ids
                    doc_to_include = product_product_docs.filtered(lambda d: d.attached_on == "inside") or product_template_docs.filtered(
                        lambda d: d.attached_on == "inside"
                    )
                    included_product_docs = included_product_docs | doc_to_include
                    doc_line_id_mapping.update({doc.id: line.id for doc in doc_to_include})

                if not has_header and not included_product_docs and not has_footer:
                    continue

                writer = PdfFileWriter()
                if has_header:
                    self._add_pages_to_writer(writer, base64.b64decode(header_record.sale_header))
                if included_product_docs:
                    for doc in included_product_docs:
                        self._add_pages_to_writer(writer, base64.b64decode(doc.datas), doc_line_id_mapping[doc.id])
                self._add_pages_to_writer(writer, initial_stream.getvalue())
                if has_footer:
                    self._add_pages_to_writer(writer, base64.b64decode(footer_record.sale_footer))

                form_fields = self._get_form_fields_mapping(order, doc_line_id_mapping)
                pdf.fill_form_fields_pdf(writer, form_fields=form_fields)
                with io.BytesIO() as _buffer:
                    writer.write(_buffer)
                    stream = io.BytesIO(_buffer.getvalue())
                result[order.id].update({"stream": stream})

        return result
