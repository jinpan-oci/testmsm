import html
import json
import logging
from urllib.parse import unquote_plus

from bs4 import BeautifulSoup
from odoo import SUPERUSER_ID, _, http
from odoo.http import Response, request

_logger = logging.getLogger(__name__)


class HerculeController(http.Controller):
    # ---------------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------------

    # function to parse the product description from the json
    # return a list of labels and a list of other variables used in the description
    def _parse_product_desc(
        self,
        data,
    ):
        try:
            label_ids_list = []
            temp_list = []
            other_var_list = []

            options = data.get("opt", False)
            answers = data.get("answers", False)

            other_var_list.append([data.get("landmark_text", False)])

            temp_list.append(data.get("lig_largeur_label", False))
            temp_list.append(" : ")
            temp_list.append(data.get("L", False))
            other_var_list.append(temp_list)
            temp_list = []

            temp_list.append(data.get("lig_hauteur_label", False))
            temp_list.append(" : ")
            temp_list.append(data.get("H", False))
            other_var_list.append(temp_list)
            temp_list = []

            temp_list.append(data.get("id", False))
            temp_list.append(data.get("label", False))
            temp_list.append(data.get("memo", False))
            label_ids_list.append(temp_list)

            if options:
                for option in options:
                    if option.get("art_imp_vente", True) and option.get("art_visible", True):
                        variables = option.get("variables", [])
                        temp_list = []
                        temp_list.append(option.get("id", False))
                        temp_list.append(option.get("label", False))
                        second_temp_list = []
                        for variable in variables:
                            if variable.get("var_imp_vente", True) and variable.get("var_visible", True):
                                if variable.get("label"):
                                    temp_var_list = []
                                    temp_var_list.append(variable.get("id", False))
                                    temp_var_list.append(variable.get("label", False))
                                    temp_var_list.append(float(variable.get("value", 0.0)))
                                    second_temp_list.append(temp_var_list)
                        if second_temp_list:
                            temp_list.append(second_temp_list)
                        if float(option.get("lig_prix_net", 0.0)):
                            temp_list.append(float(option.get("lig_prix_net", 0.0)))
                        label_ids_list.append(temp_list)

            if answers:
                for answer in answers:
                    if answer.get("art_imp_vente", True):
                        temp_list = []
                        temp_list.append(answer.get("id", False))
                        temp_list.append(answer.get("label", False))
                        label_ids_list.append(temp_list)

            return label_ids_list, other_var_list
        except Exception as e:
            _logger.error(f"Error while parsing product desc: {e}")
            return False

    # function to find/create label, title, product and return a list of them or original values
    def _prepare_matching_list(self, label_ids_list, is_recursive=False):
        try:
            # get the value of the parameter to auto complete the label and title
            # means we are allowed to create new label, title, product if they don't exist
            auto_complete_bool = request.env["ir.config_parameter"].sudo().get_param("autocomplete_desc_matrix", False)
            matching_list = []
            for label in label_ids_list:
                temp_list = []

                # search for the product in the database
                matching_product = request.env["hercule.product"].sudo().search([("name", "=", label[0])], limit=1)
                matching_product_title = False
                matching_product_label = False

                # does the product have a title and a label ?
                if matching_product:
                    if matching_product.title_id:
                        matching_product_title = matching_product.title_id
                    if matching_product.label_id:
                        matching_product_label = matching_product.label_id

                # if the product doesn't have a title or a label,
                # we search for them in the database by their origin value
                if len(label) > 2 and isinstance(label[2], str) and (not matching_product_label or not matching_product_title):
                    if not matching_product_label:
                        matching_product_label = request.env["hercule.label"].sudo().search([("origin_label", "=", label[2])], limit=1)
                    if not matching_product_title:
                        matching_product_title = request.env["hercule.title"].sudo().search([("origin_title", "=", label[1])], limit=1)

                    # if the title or the label doesn't exist, we create them if we are allowed to
                    if not matching_product_label and not is_recursive:
                        matching_product_label = request.env["hercule.label"].sudo().create({"origin_label": label[2]}) if auto_complete_bool else False
                    if not matching_product_title and not is_recursive:
                        matching_product_title = request.env["hercule.title"].sudo().create({"origin_title": label[1]}) if auto_complete_bool else False

                # do the same but for single label product
                elif not matching_product_label:
                    matching_product_label = request.env["hercule.label"].sudo().search([("name", "=", label[1])], limit=1)
                    if not matching_product_label:
                        matching_product_label = request.env["hercule.label"].sudo().create({"origin_label": label[1]}) if auto_complete_bool else False

                # if the product doesn't exist, we create it if we are allowed to
                # using the label and title we just created or found
                if not matching_product:
                    matching_product = (
                        request.env["hercule.product"]
                        .sudo()
                        .create(
                            {
                                "sequence": 0,
                                "name": label[0],
                                "title_id": (matching_product_title.id if matching_product_title else False),
                                "label_id": (matching_product_label.id if matching_product_label else False),
                            }
                        )
                        if auto_complete_bool
                        else False
                    )

                # if product now exist, we store it's value in a list to further use it
                if matching_product:
                    temp_list.append(matching_product.sequence)
                    temp_list.append(matching_product.name)
                    if matching_product_title:
                        temp_list.append(matching_product_title.name if matching_product_title.name else matching_product_title.origin_title)
                    elif not matching_product_title and len(label) >= 3:
                        if isinstance(label[2], str):  # mean there is a title just not in the matrix
                            temp_list.append(label[1])
                    temp_list.append(matching_product_label.name if matching_product_label.name else matching_product_label.origin_label)

                # if product doesn't exist, we store the values from the json
                else:
                    temp_list.append(999999)
                    temp_list.append(label[0])
                    temp_list.append(label[1])
                    if len(label) > 2:
                        if not isinstance(label[2], list):
                            temp_list.append(label[2])

                # if third value is a list, means we have to recursively call the function
                if len(label) > 2 and isinstance(label[2], list):
                    temp_list.append(self._prepare_matching_list(label[2], True))

                if matching_product_label and (matching_product_label.show_price or is_recursive) and isinstance(label[-1], float):
                    temp_list.append(label[-1])

                matching_list.append(temp_list)

            # return the list, should look like:
            # [
            #   [sequence, name, title, label],
            #   [sequence, name, title, label, [
            #           variables(same format coz recursive)
            #       ]
            #   ]
            # ]
            if not is_recursive:
                matching_list.append([999998, "NoID", "<strong>Votre Projet:</strong>"])
            return matching_list
        except Exception as e:
            _logger.error(f"Error while preparing matching list: {e}")
            return False

    # trie par séquence en gardant le premier élement en premier
    def _sort_list_by_sequence(self, matching_list):
        try:
            sorted_list = sorted(matching_list[1:], key=lambda x: x[0])
            sorted_list.insert(0, matching_list[0])
            for i in range(1, len(sorted_list)):
                if len(sorted_list[i]) > 3 and isinstance(sorted_list[i][3], list):
                    sorted_list[i][3] = sorted(sorted_list[i][3], key=lambda x: x[0])
            return sorted_list
        except Exception as e:
            _logger.error(f"Error while sorting list by sequence: {e}")
            return False

    def _build_desc(self, matching_list, other_var_list=None, is_recursive=False):
        try:
            desc = ""
            for label in matching_list:
                if label == matching_list[0] and not is_recursive:
                    desc += str(label[2]) if len(label) > 2 else ""
                    if other_var_list:
                        desc += "<br/>"
                        for other_vars in other_var_list:
                            if other_vars[0]:
                                for other_var in other_vars:
                                    desc += str(other_var)
                                desc += "<br/>"
                        desc += str(label[3]) + "<br/>" if len(label) > 3 else "<br/>"
                    desc += "<br/>"
                elif isinstance(label[-1], float):
                    if label[-1] != 0.0 and not is_recursive:
                        desc += str(label[2]) + " prix : " + str(label[-1]) + _(" € excl. taxes") + "<br/>" if len(label) > 2 else ""
                    elif label[-1] != 0.0 and is_recursive:
                        desc += str(label[2]) + _(" qté : ") + str(label[-1]) + "<br/>" if len(label) > 2 else ""
                    else:
                        desc += str(label[2]) + "<br/>" if len(label) > 2 else ""
                    if len(label) > 1 and isinstance(label[-2], list):
                        desc += self._build_desc(label[-2], is_recursive=True)
                elif isinstance(label[-1], list):
                    desc += label[2] + " : <br/>" if len(label) > 2 else ""
                    desc += self._build_desc(label[-1], is_recursive=True)
                else:
                    desc += str(label[2]) + "<br/>" if len(label) > 2 else ""

            # remplace les caractères spéciaux xml par leur valeur normale
            desc = html.unescape(desc)
            # je ne comprends pas comment des \n et des <br> se retrouvent dans un field html
            # surement de la mise en page des fields html qui n'est pas désirée ici
            desc = desc.replace("\n", "").replace("<br>", "<br/>")
            desc = desc.replace("</br>", "").replace("False<br/>", "")
            # retire toutes les balises <p> et </p> pour éviter les sauts de ligne
            desc = desc.replace("<p>", "").replace("</p>", "")
            # ne garde que celles du debut et de fin
            desc = "<p>" + desc + "</p>"
            return desc
        except Exception as e:
            _logger.error(f"Error while building desc: {e}")
            return False

    def _html_to_text(self, html):
        try:
            soup = BeautifulSoup(html, "html.parser")
            return soup.get_text()
        except Exception as e:
            _logger.error(f"Error while converting html to text: {e}")
            return False

    def _find_matching_category(self, full_code):
        try:
            category = False
            while full_code and not category:
                category = request.env["hercule.category"].sudo().search([("full_code", "=", full_code)], limit=1)
                full_code = full_code[:-3]

            if not category:
                category = request.env["hercule.category"].sudo().search([("full_code", "=", False)], limit=1)

            return category.categ_id.id if category else False
        except Exception as e:
            _logger.error(f"Error while finding matching category: {e}")
            return False

    # ---------------------------------------------------------------------------
    # Public methods
    # ---------------------------------------------------------------------------
    @http.route(
        [
            "/hercule/create_product_and_sol",
            "/hercule/create_product_and_sol/<int:company_id>/<int:order_id>",
        ],
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def create_product_and_sol(self, company_id=None, order_id=None, **post):
        data = json.loads(unquote_plus(request.params.get("xParams")))
        data_to_log = data.copy()
        data_to_log["rawCarpentryData"] = "removed because it is too long"
        data_to_log["drawimg_base64"] = "removed because it is too long"
        _logger.info(f"Data received: {data_to_log}")

        try:
            full_code = data.get("id", False)

        except Exception as e:
            _logger.error(f"Error while getting full_code: {e}")
            return Response(
                response=f"Error while getting catalog and fart_code: {e}",
                content_type="application/json;charset=utf-8",
                status=500,
            )

        try:
            categ_id = self._find_matching_category(full_code)
            if not categ_id:
                return Response(
                    response="Error while finding matching category,\n"
                    + "you must configure a default category with empty full code in:\n"
                    + "Sale -> Configuration -> Hercule -> Category Matrix",
                    content_type="application/json;charset=utf-8",
                    status=500,
                )

        except Exception as e:
            _logger.error(f"Error while getting categ_id: {e}")
            return Response(
                response=f"Error while getting categ_id: {e}",
                content_type="application/json;charset=utf-8",
                status=500,
            )

        try:
            old_desc = data.get("full_product_descriptive_text", False)
            html_desc = ""
            parsed_ids, additionnal_values = self._parse_product_desc(data)
            mapping_list = self._prepare_matching_list(parsed_ids)
            mapping_list = self._sort_list_by_sequence(mapping_list)
            html_desc = self._build_desc(mapping_list, additionnal_values)
            desc = self._html_to_text(html_desc)
            _logger.info(f"Description: {html_desc}")

        except Exception as e:
            _logger.error(f"Error while getting desc: {e}")

        try:
            route_id = request.env["ir.config_parameter"].with_company(company_id).with_user(SUPERUSER_ID).sudo().get_param("hp5_default_route_id", 1)

        except Exception as e:
            _logger.error(f"Error while getting desc and route_id: {e}")
            return Response(
                response=f"Error while getting desc and route_id: {e}",
                content_type="application/json;charset=utf-8",
                status=500,
            )

        try:
            product = (
                request.env["product.product"]
                .with_company(company_id)
                .with_user(SUPERUSER_ID)
                .sudo()
                .create(
                    {
                        "name": data.get("label"),
                        "image_1920": data.get("drawimg_base64"),
                        "type": "product",
                        "standard_price": data.get("total_unit_purchase_price"),
                        "list_price": data.get("total_unit_sale_price"),
                        "description_sale": html_desc,
                        "categ_id": int(categ_id) if categ_id else None,
                        "product_source": "hercule pro",
                        # match default values :taxes ids ?
                    }
                )
            )
            routes = product.route_ids.ids
            if int(route_id) not in routes:
                routes.append(int(route_id))

            product.write({"route_ids": [(6, 0, routes)]})

            product_template_id = product.product_tmpl_id.id

        except Exception as e:
            _logger.error(f"Error while creating product: {e}")
            return Response(
                response=f"Error while creating product: {e}",
                content_type="application/json;charset=utf-8",
                status=500,
            )

        try:
            supplier_info = data.get("supplier_infos", {})
            if supplier_info:
                partner = (
                    request.env["res.partner"]
                    .with_company(company_id)
                    .with_user(SUPERUSER_ID)
                    .sudo()
                    .search([("name", "=", supplier_info.get("raison_sociale"))], limit=1)
                )
                if not partner:
                    partner = (
                        request.env["res.partner"].with_company(company_id).with_user(SUPERUSER_ID).sudo().search([("email", "=", supplier_info.get("email"))], limit=1)
                    )

                if not partner:
                    partner = (
                        request.env["res.partner"]
                        .with_company(company_id)
                        .with_user(SUPERUSER_ID)
                        .sudo()
                        .create(
                            {
                                "name": supplier_info.get("raison_sociale"),
                                "email": supplier_info.get("email"),
                                "phone": supplier_info.get("tel"),
                                "street": supplier_info.get("adr"),
                                "city": supplier_info.get("city"),
                                "zip": supplier_info.get("post_code"),
                            }
                        )
                    )

        except Exception as e:
            _logger.error(f"Error while creating partner: {e}")
            return Response(
                response=f"Error while creating partner: {e}",
                content_type="application/json;charset=utf-8",
                status=500,
            )

        try:
            request.env["product.supplierinfo"].with_company(company_id).with_user(SUPERUSER_ID).sudo().create(
                {
                    "partner_id": partner.id,
                    "product_name": product.name,
                    "product_code": product.default_code,
                    "product_tmpl_id": product_template_id,
                    "product_id": product.id,
                    "price": data.get("total_unit_purchase_price"),
                    "delay": 7,
                    "min_qty": 1,
                    "product_uom": product.uom_id.id,
                }
            )

        except Exception as e:
            _logger.error(f"Error while creating product supplierinfo: {e}")
            return Response(
                response=f"Error while creating product supplierinfo: {e}",
                content_type="application/json;charset=utf-8",
                status=500,
            )

        try:
            # Création de la ligne de commande (sale order line)
            request.env["sale.order"].with_company(company_id).with_user(SUPERUSER_ID).sudo().browse(order_id).sudo().write(
                {
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "description_text": desc,
                                "description_html": html_desc,
                                "name": desc,  # old_desc
                                "product_uom_qty": data.get("totals").get("qty", 1),
                                "price_unit": data.get("total_unit_sale_price", 0),
                                "full_code": full_code,
                                "hercule_line": str(data) if data else False,
                            },
                        )
                    ]
                }
            )

        except Exception as e:
            _logger.error(f"Error while creating sale order line: {e}")
            return Response(
                response=f"Error while creating sale order line: {e}",
                content_type="application/json;charset=utf-8",
                status=500,
            )

        return Response(
            content_type="application/json;charset=utf-8",
            status=200,
        )
