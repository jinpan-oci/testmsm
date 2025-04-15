from odoo import http
from odoo.http import request


class ModuleUpdaterController(http.Controller):
    # create a route that when recieving a list of modules on it run a bash command that update the modules
    @http.route("/update_modules", type="http", auth="none", methods=["POST"], csrf=False)
    def update_modules(self, **post):
        # get the list of modules
        try:
            modules = post.get("modules")
            module_list = modules.split(",")
            not_installed = []
            all_module_ids = request.env["ir.module.module"].sudo().search([("name", "in", module_list)])
            module_ids = request.env["ir.module.module"].sudo().search([("name", "in", module_list), ("state", "=", "installed")])
            module_ids.button_immediate_upgrade()
            if len(module_ids) < len(all_module_ids):
                for module in all_module_ids:
                    if module not in module_ids:
                        not_installed.append(module.name)
            if not_installed:
                return "OK but " + str(not_installed) + " not installed"
            return "OK"
        except Exception as e:
            return "NOK: " + str(e)


class ModuleInstallerController(http.Controller):
    # create a route that when recieving a list of modules on it run a bash command that install the modules
    @http.route("/install_modules", type="http", auth="none", methods=["POST"], csrf=False)
    def install_modules(self, **post):
        # get the list of modules
        try:
            modules = post.get("modules")
            module_list = modules.split(",")
            # run the bash command
            module_ids = request.env["ir.module.module"].sudo().search([("name", "in", module_list), ("state", "=", "uninstalled")])
            module_ids.button_immediate_install()
            return "OK"
        except Exception as e:
            return "NOK: " + str(e)
