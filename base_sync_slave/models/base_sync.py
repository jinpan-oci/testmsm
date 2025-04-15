import base64
import logging
import xmlrpc.client

from odoo import SUPERUSER_ID, _, fields, models

_logger = logging.getLogger(__name__)

READ_OPTIONS = {
    "import_skip_records": [],
    "import_set_empty_fields": [],
    "fallback_values": {},
    "name_create_enabled_fields": {},
    "encoding": "",
    "separator": "",
    "quoting": '"',
    "date_format": "",
    "datetime_format": "",
    "float_thousand_separator": ",",
    "float_decimal_separator": ".",
    "advanced": True,
    "has_headers": True,
    "keep_matches": False,
    "limit": 500,
    "sheets": [],
    "sheet": "",
    "skip": 0,
    "tracking_disable": True,
}


class BaseSync(models.Model):

    _name = "base.sync"
    _description = "Base Sync"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Catalog Reference",
        required=True,
        copy=False,
        readonly=False,
        index="trigram",
        default=lambda self: _("New"),
    )
    base_sync_line_ids = fields.One2many(
        comodel_name="base.sync.line",
        inverse_name="base_sync_id",
        string="Base Sync Lines",
    )
    is_imported = fields.Boolean(string="Is Imported ?", default=False)
    has_import_started = fields.Boolean(string="Has Import Started ?", default=False)
    has_errors = fields.Boolean(string="Has Error ?", default=False)
    csv_or_xlsx = fields.Selection(
        [("csv", "CSV"), ("xlsx", "XLSX")], string="File Type"
    )

    def generate_line_ids(self, base_sync_id):
        """
        Generate line ids from xmlrpc call to master
        """
        master = self.env["base.sync.master"].search([], limit=1)
        if master:
            url = master.master_url
            db = master.master_db
            username = master.master_user
            password = master.master_api_key
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
            model_name = "base.sync"
            result = models.execute_kw(
                db,
                uid,
                password,
                model_name,
                "search_read",
                [[["id", "=", base_sync_id]]],
                {"fields": ["base_sync_line_ids", "name"]},
            )

            # create a dict with master.notification_follower_ids

            self = self.create(
                {
                    "name": result[0]["name"],
                    "base_sync_line_ids": [],
                }
            )

            self.with_user(SUPERUSER_ID).message_notify(
                body=_(
                    "A new catalog has been created, it will be automatically imported at 8pm."
                ),
                model=self._name,
                notify_author=True,
                partner_ids=[
                    partner.id for partner in master.notification_follower_ids
                ],
                res_id=self.id,
                subject=_("New Catalog"),
            )

            for line in result[0]["base_sync_line_ids"]:
                model_name = "base.sync.line"
                fields = ["file_name", "file_data", "file_number"]
                ret = models.execute_kw(
                    db, uid, password, model_name, "read", [line], {"fields": fields}
                )
                if ret:
                    # Decode the binary data ?
                    binary_data = ret[0]["file_data"]
                    file_name = ret[0]["file_name"]
                    file_number = ret[0]["file_number"]
                    if ".xlsx" in file_name:
                        self.csv_or_xlsx = "xlsx"
                        self.base_sync_line_ids.create(
                            {
                                "name": file_name[0:-5],
                                "file_name": file_name,
                                "file_data": binary_data,
                                "file_number": file_number,
                                "base_sync_id": self.id,
                            }
                        )
                    elif ".csv" in file_name:
                        self.csv_or_xlsx = "csv"
                        self.base_sync_line_ids.create(
                            {
                                "name": file_name[0:-4],
                                "file_name": file_name,
                                "file_data": binary_data,
                                "file_number": file_number,
                                "base_sync_id": self.id,
                            }
                        )
        else:
            pass

    def import_csv(self, line):
        """
        Import csv stored in catalog_line_ids, using base_import transient model
        """
        base_import_id = self.env["base_import.import"].create(
            {
                "res_model": line.file_name[0:-4],
                "file": base64.b64decode(line.file_data),
                "file_name": line.file_name,
                "file_type": "text/csv",
            }
        )

        model_fields_tree = base_import_id.get_fields_tree(base_import_id.res_model)
        file_data = base_import_id._read_csv(READ_OPTIONS)
        preview = [
            file_data[1][1 + i]
            for i in range(9 if len(file_data[1][1:]) > 9 else len(file_data[1][1:]))
        ]
        headers = file_data[1][0]
        headers_without_empty = file_data[1][0]
        headers_types = base_import_id._extract_headers_types(
            headers, preview, READ_OPTIONS
        )
        mapping_suggestions = base_import_id._get_mapping_suggestions(
            headers, headers_types, model_fields_tree
        )
        for field in mapping_suggestions:
            if not mapping_suggestions[field]:
                for i in range(len(headers_without_empty)):
                    if headers_without_empty[i] == field[1]:
                        headers_without_empty[i] = False
        # import pdb; pdb.set_trace()
        # execute import wich returns a list of errors
        line.error_list = base_import_id.execute_import(
            headers_without_empty, headers, READ_OPTIONS
        )
        if "Read timed out." in line.error_list:
            self.has_errors = False
            self.import_csv(line)
        if "'rows'" in line.error_list or "'error'" in line.error_list:
            self.has_errors = True
        else:
            line.is_imported = True

    def import_xlsx(self, line):
        """
        Import xlsx stored in catalog_line_ids, using base_import transient model
        """
        base_import_id = self.env["base_import.import"].create(
            {
                "res_model": line.file_name[0:-5],
                "file": base64.b64decode(line.file_data),
                "file_name": line.file_name,
                "file_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        )

        model_fields_tree = base_import_id.get_fields_tree(base_import_id.res_model)
        file_data = base_import_id._read_xls(READ_OPTIONS)
        preview = [
            file_data[1][1 + i]
            for i in range(9 if len(file_data[1][1:]) > 9 else len(file_data[1][1:]))
        ]
        headers = file_data[1][0]
        headers_without_empty = file_data[1][0]
        headers_types = base_import_id._extract_headers_types(
            headers, preview, READ_OPTIONS
        )
        mapping_suggestions = base_import_id._get_mapping_suggestions(
            headers, headers_types, model_fields_tree
        )
        for field in mapping_suggestions:
            if not mapping_suggestions[field]:
                for i in range(len(headers_without_empty)):
                    if headers_without_empty[i] == field[1]:
                        headers_without_empty[i] = False
        # import pdb; pdb.set_trace()
        # execute import wich returns a list of errors
        line.error_list = base_import_id.execute_import(
            headers_without_empty, headers, READ_OPTIONS
        )
        if "'rows'" in line.error_list:
            line.is_imported = False
        else:
            line.is_imported = True

    def notify_good_import(self):
        master = self.env["base.sync.master"].search([], limit=1)
        self.with_user(SUPERUSER_ID).message_notify(
            body=_("The new catalog has been imported."),
            model=self._name,
            notify_author=True,
            partner_ids=[partner.id for partner in master.notification_follower_ids],
            res_id=self.id,
            subject=_("New Catalog"),
        )

    def notify_bad_import(self):
        master = self.env["base.sync.master"].search([], limit=1)
        self.with_user(SUPERUSER_ID).message_notify(
            body=_("The new catalog import has encountered errors."),
            model=self._name,
            notify_author=True,
            partner_ids=[partner.id for partner in master.notification_follower_ids],
            res_id=self.id,
            subject=_("New Catalog"),
        )

    def import_first_file(self):
        # line = record.base_sync_line_ids.filtered(lambda l_line: l_line.is_imported == False)[0]
        line = self.env["base.sync.line"].search(
            [("base_sync_id", "=", self.id), ("is_imported", "=", False)], limit=1
        )
        if line:
            if self.csv_or_xlsx == "csv":
                self.with_context(lang="en_US").import_csv(line)
            elif self.csv_or_xlsx == "xlsx":
                self.with_context(lang="en_US").import_xlsx(line)
            if not line.is_imported:
                self.has_errors = True
                self.notify_bad_import()
            if line.is_imported and self.has_errors:
                self.has_errors = False
            self.has_import_started = True
        else:
            self.has_errors = False
            self.is_imported = True
            self.notify_good_import()

    def test_import_first_file(self):
        """
        Test import first file
        """
        for record in self:
            record.import_first_file()
        return True

    def _action_cron(self):
        """
        Action to be executed by cron
        """
        for record in self.search(
            [("is_imported", "=", False), ("has_errors", "=", False)], limit=1
        ):
            record.import_first_file()

    def _action_cron_2(self):
        """
        Action to be executed by cron
        """
        for record in self.search(
            [
                ("is_imported", "=", False),
                ("has_errors", "=", False),
                ("has_import_started", "=", True),
            ],
            limit=1,
        ):
            record.import_first_file()
