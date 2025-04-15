import logging
from datetime import datetime

import requests
from odoo import fields, models

_logger = logging.getLogger(__name__)


class ModuleUpdaterLine(models.Model):
    _name = "module.updater.line"
    _description = "Module Updater Line: contain servers url"
    _order = "name asc"

    module_updater_id = fields.Many2one("module.updater", string="Module Updater")
    name = fields.Char(string="Name")

    url = fields.Char(string="Url")

    response_date = fields.Datetime(string="Response Date")
    response = fields.Char(string="Response")

    def update_module(self):
        for record in self:
            modules = ""
            for tag in record.module_updater_id.update_ids:
                modules += tag.name + ","
            if modules:
                modules = modules[:-1]
            # send http request to the url + /update_modules with the list of modules as kw
            if modules and record.url:
                _logger.info(f"({record.name})Update Request Sent.")
                response = requests.post(record.url + "/update_modules", data={"modules": modules})
                # print the response
                record.response = response.text
                record.response_date = datetime.now()
                _logger.info(f"({record.name})Update Response: %s", response.text)

    def install_module(self):
        for record in self:
            modules = ""
            for tag in record.module_updater_id.install_ids:
                modules += tag.name + ","
            if modules:
                modules = modules[:-1]
            # send http request to the url + /install_modules with the list of modules as kw
            if modules and record.url:
                _logger.info(f"({record.name})Install Request Sent.")
                response = requests.post(record.url + "/install_modules", data={"modules": modules})
                # print the response
                record.response = response.text
                record.response_date = datetime.now()
                _logger.info(f"({record.name})Install Response: %s", response.text)
