import re
from datetime import datetime

from bs4 import BeautifulSoup
from odoo import api, models
import logging

_logger = logging.getLogger(__name__)




class MailMessage(models.Model):
    _inherit = "mail.message"

    def extract_city_and_postal_code(self, text):
        match = re.search(r"(.+?)\((\d+)\)", text)
        if match:
            city = match.group(1).strip()
            postal_code = match.group(2)
            return True, city, postal_code
        else:
            return False, text

    def get_source_id(self, name):
        source = self.env["utm.source"].search([("name", "=", name)], limit=1)
        if source:
            return source.id
        else:
            return self.env["utm.source"].create({"name": name}).id

    def parse_mail(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        datas = {}
        corr = {
            "Nom": "Nom",
            "Tel": "Tel",
            "Mail": "Mail",
            "Ville": "Ville",
            "A contacter par": "A contacter par",
            "Magasin": "Magasin",
            "Souhaite": "Souhaite",
            "Delai": "Delai",
            "Produit": "Produit",
            "Sous Produit": "Sous Produit",
            "Description": "Description",
            "Financement": "Financement",
            "Newsletter": "Newsletter",
            "RGPD": "RGPD",
            "Offre du moment": "Offre du moment",
        }

        parse = soup.find_all(
            "td",
            attrs={
                "width": 300,
                "height": 20,
                # "style": "border:none; border-bottom:solid white 1.0pt; padding:0cm 0cm 0cm 0cm;"
            },
        )
        _logger.info(f'{parse}= parse')

        for r in parse:
            prev = r.find_previous("td").text.strip()
            _logger.info(f'{prev}= prev')
            _logger.info(f'{r.text.strip()}= r.text.strip()')   
            data = r.text.strip()
            if prev in corr:
                if prev == "Ville":
                    extract = self.extract_city_and_postal_code(data)
                    if extract[0]:
                        datas[corr[prev]] = extract[1]
                        datas["Code Postal"] = extract[2]
                    else:
                        datas[corr[prev]] = data
                else:
                    datas[corr[prev]] = data
        return datas

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            internal_notes = ""
            if (
                rec.record_name
                == "[Contact Monsieur Store] Nouvelle demande de contact"
                and (rec.model == "crm.lead" and rec.res_id)
                and rec.message_type == "email"
            ):
                crm_lead_id = self.env["crm.lead"].browse(rec.res_id)
                if crm_lead_id:
                    datas = self.parse_mail(rec.body)
                    _logger.info(f'{datas}= datas')
                    if not datas:
                        continue

                    for prev, data in datas.items():
                        if prev in [
                            "Delai",
                            "Souhaite",
                            "Magasin",
                            "A contacter par",
                            "Produit",
                            "Sous Produit",
                            "Description",
                            "Financement",
                            "Newsletter",
                            "RGPD",
                            "Offre du moment",
                        ]:
                            internal_notes += f"{prev}: {data}<br>"

                    crm_lead_id.write(
                        {
                            "name": "{}_{}_{}".format(
                                datas["Nom"], datas["Produit"], datas["Ville"]
                            ),
                            "contact_name": datas["Nom"],
                            "email_from": datas["Mail"],
                            "zip": datas["Code Postal"],
                            "city": datas["Ville"],
                            "source_id": self.get_source_id("LEAD INTERNET"),
                            "description": internal_notes,
                        }
                    )
                    if datas["Tel"].startswith("06") or datas["Tel"].startswith("07"):
                        crm_lead_id.write({"mobile": datas["Tel"]})
                    else:
                        crm_lead_id.write({"phone": datas["Tel"]})

                    # to prevent odoo from dumping similar emails, add a datestamp to the mail subject
                    rec.record_name = (
                        rec.record_name + " - " + datetime.now().strftime("%d/%m/%Y")
                    )
                    rec.subject = (
                        rec.subject + " - " + datetime.now().strftime("%d/%m/%Y")
                    )

        return res
