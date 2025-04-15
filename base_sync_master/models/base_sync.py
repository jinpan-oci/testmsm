import base64
import datetime
import io
import json
import operator

import requests
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools import pycompat
from odoo.tools.misc import xlsxwriter
from odoo.tools.translate import _

IMAGE_URL_LIST = [
    "image_1920_url",
]


class BaseSync(models.Model):

    _name = "base.sync"
    _description = "Base To Sync"

    name = fields.Char(
        string="Catalog Reference",
        required=True,
        copy=False,
        readonly=False,
        index="trigram",
        default=lambda self: _("New"),
    )
    base_sync_template_id = fields.Many2one(
        "base.sync.template", string="Base Sync Template"
    )
    base_sync_line_ids = fields.One2many(
        comodel_name="base.sync.line",
        inverse_name="base_sync_id",
        string="Base Sync Lines",
    )
    got_error = fields.Boolean(string="Got Error", default=False)

    # TODO change 'master_catalog_id' to 'base_sync_id' in slave controller

    # ------- Notify Slaves ------- #

    def notify_slaves(self):
        urls = []
        for slave in self.env["base.sync.slaves"].search([]):
            if slave.slave_url:
                url = slave.slave_url
                if url[-1] == "/":
                    url = url[:-1]
                if url[-4:] != ".com" and url[-4:] != ".app":
                    self.got_error = True
                    raise UserError(
                        _(
                            "Invalid URL: "
                            + url
                            + ", please provide a valid URL endind with .com and Publish again."
                        )
                    )
                else:
                    self.got_error = False
                url = url + "/sync/webhooks/base_sync"
                urls.append(url)
            else:
                self.got_error = True
                raise UserError(
                    _(
                        "Please provide a URL for the slave: "
                        + slave.name
                        + ", and Publish again."
                    )
                )

        for url in urls:
            self.notify_slave(url)

    def notify_slave(self, url):
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "base_sync_id": self.id,
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            self.got_error = False
            print("Success: ", response.text)
        else:
            self.got_error = True
            print("Request Failed: ", response.status_code, response.text)

    # ------- XLSX Export ------- #

    def from_data_xlsx(self, fields, rows):
        with ExportXlsxWriter(fields, len(rows)) as xlsx_writer:
            for row_index, row in enumerate(rows):
                for cell_index, cell_value in enumerate(row):
                    xlsx_writer.write_cell(row_index + 1, cell_index, cell_value)

        return xlsx_writer.value

    def generate_xlsx(self, data):
        params = json.loads(data)
        model, fields, ids, domain, import_compat = operator.itemgetter(
            "model", "fields", "ids", "domain", "import_compat"
        )(params)

        Model = self.env[model].with_context(
            import_compat=import_compat, **params.get("context", {})
        )
        if not Model._is_an_ordinary_table():
            fields = [field for field in fields if field["name"] != "id"]

        field_names = [f["name"] for f in fields]

        if import_compat:
            columns_headers = field_names

        records = (
            Model.browse(ids)
            if ids
            else Model.search(domain, offset=0, limit=False, order=False)
        )

        export_data = records.export_data(field_names).get("datas", [])

        for image_url in IMAGE_URL_LIST:
            if image_url in columns_headers:
                columns_headers[columns_headers.index(image_url)] = columns_headers[
                    columns_headers.index(image_url)
                ][:-4]

        response_data = self.from_data_xlsx(columns_headers, export_data)

        b64_data = base64.b64encode(response_data)
        return b64_data

    # ------- CSV Export ------- #

    def from_data_csv(self, fields, rows):
        fp = io.BytesIO()
        writer = pycompat.csv_writer(fp, quoting=1)

        writer.writerow(fields)

        for data in rows:
            row = []
            for d in data:
                # Spreadsheet apps tend to detect formulas on leading =, + and -
                if isinstance(d, str) and d.startswith(("=", "-", "+")):
                    d = "'" + d

                row.append(pycompat.to_text(d))
            writer.writerow(row)

        return fp.getvalue()

    def generate_csv(self, data):
        params = json.loads(data)
        model, fields, ids, domain, import_compat = operator.itemgetter(
            "model", "fields", "ids", "domain", "import_compat"
        )(params)

        Model = self.env[model].with_context(
            import_compat=import_compat, **params.get("context", {})
        )
        if not Model._is_an_ordinary_table():
            fields = [field for field in fields if field["name"] != "id"]

        field_names = [f["name"] for f in fields]

        if import_compat:
            columns_headers = field_names

        records = (
            Model.browse(ids)
            if ids
            else Model.search(domain, offset=0, limit=False, order=False)
        )

        export_data = records.export_data(field_names).get("datas", [])

        for image_url in IMAGE_URL_LIST:
            if image_url in columns_headers:
                columns_headers[columns_headers.index(image_url)] = columns_headers[
                    columns_headers.index(image_url)
                ][:-4]

        response_data = self.from_data_csv(columns_headers, export_data)

        b64_data = base64.b64encode(response_data)
        return b64_data

    # ------- Prepare Dicts ------- #

    def prepare_dict_for_ids_to_export(self):
        parent_ids = (
            self.env["product.category"]
            .search([("is_category_intended_for_shared_catalog", "=", True)])
            .ids
        )

        product_category_ids = []
        product_template_ids = []
        product_template_attribute_line_ids = []
        product_attribute_ids = []
        uom_product_category_ids = []
        product_tag_ids = []
        res_partner_category_ids = []
        res_partner_ids = []
        res_country_ids = []
        res_partner_parent_ids = []
        product_supplierinfo_ids = []
        product_pricelist_ids = []
        ids_to_export_dict = {}

        for category in self.env["product.category"].search([]):
            if int(category.parent_path.split("/")[0]) in parent_ids:
                product_category_ids.append(category.id)

        for product in self.env["product.template"].search([]):
            if product.categ_id.id in product_category_ids:

                product_template_ids.append(product.id)

                if product.attribute_line_ids:
                    for attribute in product.attribute_line_ids:
                        if attribute.id not in product_template_attribute_line_ids:
                            product_template_attribute_line_ids.append(attribute.id)

                        if attribute.attribute_id.id not in product_attribute_ids:
                            product_attribute_ids.append(attribute.attribute_id.id)

                if product.uom_id.category_id.id:
                    if product.uom_id.category_id.id not in uom_product_category_ids:
                        uom_product_category_ids.append(product.uom_id.category_id.id)

                if product.product_tag_ids:
                    for tag in product.product_tag_ids:
                        if tag.id not in product_tag_ids:
                            product_tag_ids.append(tag.id)

        for supplierinfo in self.env["product.supplierinfo"].search([]):
            if supplierinfo.product_tmpl_id.id in product_template_ids:
                product_supplierinfo_ids.append(supplierinfo.id)

                if supplierinfo.partner_id and supplierinfo.partner_id.parent_id:
                    if supplierinfo.partner_id.parent_id.id not in res_partner_ids:
                        res_partner_parent_ids.append(
                            supplierinfo.partner_id.parent_id.id
                        )

                    if supplierinfo.partner_id.parent_id.country_id.id not in res_country_ids:
                        res_country_ids.append(
                            supplierinfo.partner_id.parent_id.country_id.id
                        )

                if supplierinfo.partner_id.id not in res_partner_ids:
                    res_partner_ids.append(supplierinfo.partner_id.id)

                if supplierinfo.partner_id.country_id.id not in res_country_ids:
                    res_country_ids.append(supplierinfo.partner_id.country_id.id)

                if supplierinfo.partner_id.category_id:
                    for category in supplierinfo.partner_id.category_id:
                        if category.id not in res_partner_category_ids:
                            res_partner_category_ids.append(category.id)

        for pricelist in self.env["product.pricelist"].search([]):
            for item in pricelist.item_ids:
                if item.categ_id and item.categ_id.id in product_category_ids:
                    if pricelist.id not in product_pricelist_ids:
                        product_pricelist_ids.append(pricelist.id)

                if (
                    item.product_tmpl_id
                    and item.product_tmpl_id.id in product_template_ids
                ):
                    if pricelist.id not in product_pricelist_ids:
                        product_pricelist_ids.append(pricelist.id)

                if (
                    item.product_id
                    and item.product_id.product_tmpl_id.id in product_template_ids
                ):
                    if pricelist.id not in product_pricelist_ids:
                        product_pricelist_ids.append(pricelist.id)

        ids_to_export_dict["product.category"] = product_category_ids
        ids_to_export_dict["uom.category"] = uom_product_category_ids
        ids_to_export_dict["product.tag"] = product_tag_ids
        ids_to_export_dict["product.template"] = product_template_ids
        ids_to_export_dict["product.template.attribute.line"] = (
            product_template_attribute_line_ids
        )
        ids_to_export_dict["product.attribute"] = product_attribute_ids
        ids_to_export_dict["res.partner.category"] = res_partner_category_ids
        ids_to_export_dict["res.country"] = res_country_ids
        ids_to_export_dict["res.partner"] = res_partner_parent_ids + res_partner_ids
        ids_to_export_dict["product.supplierinfo"] = product_supplierinfo_ids
        ids_to_export_dict["product.pricelist"] = product_pricelist_ids

        return ids_to_export_dict

    def split_dict(self, dict_to_split, size=500):
        for key, value in dict_to_split.items():
            if len(value) > size:
                dict_to_split[key] = [
                    value[i : i + size] for i in range(0, len(value), size)
                ]
            else:
                dict_to_split[key] = [value]
        return dict_to_split

    def prepare_dict_for_catalog_line(
        self, export_line_id, ids_to_export_dict, index=0
    ):
        dict_for_catalog_line = {
            "import_compat": True,
            "context": {
                "lang": self.env.context.get("lang"),
                "tz": self.env.context.get("tz"),
                "uid": self.env.context.get("uid"),
                "allowed_company_ids": self.env.context.get("allowed_company_ids"),
            },
            "domain": [],
            "fields": [
                {
                    "name": export_line_id.export_fields[i].name,
                    "label": export_line_id.export_fields[i].name,
                }
                for i in range(len(export_line_id.export_fields))
            ],
            "groupby": [],
            "ids": ids_to_export_dict[export_line_id.resource][index],
            "model": export_line_id.resource,
        }
        return json.dumps(dict_for_catalog_line)

    # ------- Generate Base Sync Lines ------- #

    def generate_base_sync_lines(self):
        for record in self:
            record = record.with_context(lang="en_US")
            if record.base_sync_template_id:
                ids_to_export_dict = record.split_dict(
                    record.prepare_dict_for_ids_to_export()
                )
                for (
                    export_line_id
                ) in (
                    record.base_sync_template_id.base_sync_template_line_ids.ir_exports_id
                ):
                    for index in range(
                        len(ids_to_export_dict[export_line_id.resource])
                    ):
                        dict_for_catalog_line = record.prepare_dict_for_catalog_line(
                            export_line_id, ids_to_export_dict, index
                        )
                        if record.base_sync_template_id.csv_or_xlsx == "csv":
                            record.base_sync_line_ids.create(
                                {
                                    "name": export_line_id.resource,
                                    "file_number": index + 1,
                                    "base_sync_id": record.id,
                                    "file_data": record.generate_csv(
                                        dict_for_catalog_line
                                    ),
                                    "file_name": export_line_id.resource + ".csv",
                                }
                            )
                        elif record.base_sync_template_id.csv_or_xlsx == "xlsx":
                            record.base_sync_line_ids.create(
                                {
                                    "name": export_line_id.resource,
                                    "file_number": index + 1,
                                    "base_sync_id": record.id,
                                    "file_data": record.generate_xlsx(
                                        dict_for_catalog_line
                                    ),
                                    "file_name": export_line_id.resource + ".xlsx",
                                }
                            )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            rec.base_sync_template_id = (
                self.env["base.sync.template"].search(
                    [("is_default_template", "=", True)], limit=1
                )
                or None
            )
            if rec.base_sync_template_id:
                rec.name = rec.env["ir.sequence"].next_by_code(
                    "base.sync", sequence_date=None
                )
            else:
                raise UserError(_("Please create a default template first."))
        return res


class ExportXlsxWriter:

    def __init__(self, field_names, row_count=0):
        self.field_names = field_names
        self.output = io.BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output, {"in_memory": True})
        self.base_style = self.workbook.add_format({"text_wrap": True})
        self.header_style = self.workbook.add_format({"bold": True})
        self.header_bold_style = self.workbook.add_format(
            {"text_wrap": True, "bold": True, "bg_color": "#e9ecef"}
        )
        self.date_style = self.workbook.add_format(
            {"text_wrap": True, "num_format": "yyyy-mm-dd"}
        )
        self.datetime_style = self.workbook.add_format(
            {"text_wrap": True, "num_format": "yyyy-mm-dd hh:mm:ss"}
        )
        self.worksheet = self.workbook.add_worksheet()
        self.value = False
        self.float_format = "#,##0.00"
        decimal_places = [
            res["decimal_places"]
            for res in request.env["res.currency"].search_read([], ["decimal_places"])
        ]
        self.monetary_format = f'#,##0.{max(decimal_places or [2]) * "0"}'

        if row_count > self.worksheet.xls_rowmax:
            raise UserError(
                _(
                    "There are too many rows (%s rows, limit: %s) to export as Excel 2007-2013 (.xlsx) format. Consider splitting the export."
                )
                % (row_count, self.worksheet.xls_rowmax)
            )

    def __enter__(self):
        self.write_header()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def write_header(self):
        # Write main header
        for i, fieldname in enumerate(self.field_names):
            self.write(0, i, fieldname, self.header_style)
        self.worksheet.set_column(
            0, max(0, len(self.field_names) - 1), 30
        )  # around 220 pixels

    def close(self):
        self.workbook.close()
        with self.output:
            self.value = self.output.getvalue()

    def write(self, row, column, cell_value, style=None):
        self.worksheet.write(row, column, cell_value, style)

    def write_cell(self, row, column, cell_value):
        cell_style = self.base_style

        if isinstance(cell_value, bytes):
            try:
                # because xlsx uses raw export, we can get a bytes object
                # here. xlsxwriter does not support bytes values in Python 3 ->
                # assume this is base64 and decode to a string, if this
                # fails note that you can't export
                cell_value = pycompat.to_text(cell_value)
            except UnicodeDecodeError:
                raise UserError(
                    _(
                        "Binary fields can not be exported to Excel unless their content is base64-encoded. That does not seem to be the case for %s.",
                        self.field_names,
                    )[column]
                )
        elif isinstance(cell_value, (list, tuple, dict)):
            cell_value = pycompat.to_text(cell_value)

        if isinstance(cell_value, str):
            if len(cell_value) > self.worksheet.xls_strmax:
                cell_value = _(
                    "The content of this cell is too long for an XLSX file (more than %s characters). Please use the CSV format for this export.",
                    self.worksheet.xls_strmax,
                )
            else:
                cell_value = cell_value.replace("\r", " ")
        elif isinstance(cell_value, datetime.datetime):
            cell_style = self.datetime_style
        elif isinstance(cell_value, datetime.date):
            cell_style = self.date_style
        elif isinstance(cell_value, float):
            cell_style.set_num_format(self.float_format)
        self.write(row, column, cell_value, cell_style)
