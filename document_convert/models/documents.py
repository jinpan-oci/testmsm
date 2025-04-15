import base64
import requests
from odoo import models
import logging

_logger = logging.getLogger(__name__)


class Document(models.Model):
    _inherit = "documents.document"

    def load_document_from_url(self, url):
        data = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")
        self.update({"datas": data})
        self.env.cr.commit()

    def verify_and_upload_missing_doc(self, error_documents, limit):
        error_documents_object = self.browse(error_documents)
        total_error_documents_partners = len(error_documents_object.mapped("partner_id"))
        documents = self.search([("id", "in", error_documents)], limit=limit)
        Partners = documents.mapped("partner_id")
        Partners_name = "Nombre Total des documents erronés %s \nTotal de partnaire concernés %s \nNombre de partenaires à corriger dans ce lot %s \n %s" % (
            len(error_documents_object),
            total_error_documents_partners,
            len(Partners),
            [partner.name for partner in Partners],
        )

        self.env["ir.logging"].sudo().create(
            {
                "dbname": self.env.cr.dbname,
                "type": "client",
                "name": "Corriger document Erronés",
                "level": "Critical",
                "path": "Partner",
                "line": "nombre",
                "func": "verify_and_upload_missing_doc",
                "message": Partners_name,
            }
        )
        for document in documents:
            filename = document.name
            do_upload = False
            try:
                response = self.env["ir.binary"]._get_stream_from(document, filename=filename)
            except Exception as e:
                # Log the exception and treat it as an error for this document
                do_upload = True

            if do_upload and document.description:
                document.load_document_from_url(document.description)

    def retrieve_documents_with_errors(self, documents):
        _logger.info("##doc à traiter #### %s", len(documents))
        error_documents = []
        # error_documents_object = self.env['document.documents']
        for document in documents:
            try:
                filename = document.name
                response = self.env["ir.binary"]._get_stream_from(document, filename=filename)
                # Assuming an 'error' key or status code indicates an error

            except Exception as e:
                # Log the exception and treat it as an error for this document
                error_documents.append(document.id)
                # error_documents_object += document
        error_documents_object = self.browse(error_documents)
        Partners = error_documents_object.mapped("partner_id")
        Partners_name = [partner.name for partner in Partners]
        _logger.info("##doc Partners #### %s", len(Partners))
        _logger.info("##doc erronés #### %s", len(error_documents))
        _logger.info("##Partners #### %s", Partners_name)
        return error_documents
