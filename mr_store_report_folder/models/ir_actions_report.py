import io

from odoo import fields, models
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject, createStringObject

# import requests
# import base64


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    PDFdatas = fields.Binary("PDF Content", attachment=True, help="PDF content")

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        result = super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids=res_ids)
        if self._get_report(report_ref).report_name != "mr_store_report_folder.report_folder_raw":
            return result

        orders = self.env["sale.order"].browse(res_ids)

        for order in orders:
            initial_stream = result[order.id]["stream"]
            pdf_list = []
            if initial_stream:
                for attachment in order.env["ir.attachment"].search(
                    [
                        ("res_model", "=", "sale.order"),
                        ("res_id", "=", order.id),
                        ("photo_use_type", "=", "before_installation"),
                    ]
                ):
                    if attachment.mimetype == "application/pdf":
                        pdf_list.append(attachment)

                    if "SO-Sign" in attachment.name:
                        skip_vat = True

                for attachment in order.env["ir.attachment"].search(
                    [
                        ("res_model", "=", "sale.order"),
                        ("res_id", "=", order.id),
                        ("photo_use_type", "=", "with_3d"),
                    ]
                ):
                    if attachment.mimetype == "application/pdf":
                        pdf_list.append(attachment)

                    if "SO-Sign" in attachment.name:
                        skip_vat = True

                for attachment in order.env["ir.attachment"].search(
                    [
                        ("res_model", "=", "sale.order"),
                        ("res_id", "=", order.id),
                        ("photo_use_type", "=", "mesures"),
                    ]
                ):
                    if attachment.mimetype == "application/pdf":
                        pdf_list.append(attachment)

                    if "SO-Sign" in attachment.name:
                        skip_vat = True

                skip_vat = False
                for attachment in order.env["ir.attachment"].search(
                    [
                        ("res_model", "=", "sale.order"),
                        ("res_id", "=", order.id),
                        ("photo_use_type", "=", "other"),
                    ]
                ):
                    if attachment.mimetype == "application/pdf" and "SO-Sign" in attachment.name:
                        pdf_list.append(attachment)
                        skip_vat = True

                footer_vat = bool(True if order.company_id.vat_pdf and not skip_vat else False)
                # footer_gcs = bool(True if order.company_id.gsc_pdf else False)

                IrBinary = self.env["ir.binary"]
                writer = PdfFileWriter()
                self._add_pages_to_writer(writer, (initial_stream).getvalue())

                if pdf_list:
                    for pdf_file in pdf_list:
                        footer_stream = IrBinary._record_to_stream(pdf_file, "datas").read()
                        self._add_pages_to_writer(writer, footer_stream)

                if footer_vat:
                    footer_stream = IrBinary._record_to_stream(order.company_id, "vat_pdf").read()
                    self._add_1_page_to_writer(writer, footer_stream)
                # if footer_gcs:
                # footer_stream = IrBinary._record_to_stream(order.company_id, 'gsc_pdf').read()
                # self._add_pages_to_writer(writer, footer_stream)

                with io.BytesIO() as _buffer:
                    writer.write(_buffer)
                    stream = io.BytesIO(_buffer.getvalue())
                result[order.id].update({"stream": stream})

        return result

    def _add_1_page_to_writer(self, writer, document, sol_id=None):
        prefix = f"{sol_id}_" if sol_id else ""
        reader = PdfFileReader(io.BytesIO(document), strict=False)
        sol_field_names = self._get_sol_form_fields_names()
        for page_id in range(1):
            page = reader.getPage(page_id)
            if sol_id and page.get("/Annots"):
                for j in range(0, len(page["/Annots"])):
                    writer_annot = page["/Annots"][j].getObject()
                    if writer_annot.get("/T") in sol_field_names:
                        writer_annot.update({NameObject("/T"): createStringObject(prefix + writer_annot.get("/T"))})
            writer.addPage(page)
