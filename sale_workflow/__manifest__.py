
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mr Store Sale Workflow",
    "summary": "Mananage sale workflow",
    "version": "17.0.0.0.1",
    "development_status": "Beta",
    "category": "Generic Modules/Base",
    "website": "",
    "author": "Irokoo",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base","mail","sale_management"],
    "data": [
            "security/ir.model.access.csv",
            "views/sale_view.xml",
            "views/workflow_view.xml",           
            ],
}
