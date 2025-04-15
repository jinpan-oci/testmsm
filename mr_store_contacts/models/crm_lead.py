from odoo import fields, models

NEW_PARTNER_ADDRESS_FIELDS_TO_SYNC = [
    "residence_name",
    "residence_number",
    "appartment_number",
    "floor_number",
    "portal_code",
    "entry_code",
    "house_type",
]

PARTNER_ADDRESS_FIELDS_TO_SYNC = [
    "street",
    "street2",
    "city",
    "zip",
    "state_id",
    "country_id",
]

CRM_LEAD_FIELDS_TO_MERGE = [
    # UTM mixin
    "campaign_id",
    "medium_id",
    "source_id",
    # Mail mixin
    "email_cc",
    # description
    "name",
    "user_id",
    "color",
    "company_id",
    "lang_id",
    "team_id",
    "referred",
    # pipeline
    "stage_id",
    # revenues
    "expected_revenue",
    "recurring_plan",
    "recurring_revenue",
    # dates
    "create_date",
    "date_automation_last",
    "date_deadline",
    # partner / contact
    "partner_id",
    "title",
    "partner_name",
    "contact_name",
    "email_from",
    "function",
    "mobile",
    "phone",
    "website",
]


class Lead(models.Model):

    _inherit = "crm.lead"

    residence_name = fields.Char(
        "Residence Name",
        compute="_compute_partner_address_values",
        readonly=False,
        store=True,
    )

    residence_number = fields.Char(
        "Residence Number",
        compute="_compute_partner_address_values",
        readonly=False,
        store=True,
    )

    appartment_number = fields.Char(
        "Appartment Number",
        compute="_compute_partner_address_values",
        readonly=False,
        store=True,
    )

    floor_number = fields.Char(
        "Floor Number",
        compute="_compute_partner_address_values",
        readonly=False,
        store=True,
    )

    portal_code = fields.Char(
        "Portal Code",
        compute="_compute_partner_address_values",
        readonly=False,
        store=True,
    )

    entry_code = fields.Char(
        "Door Code",
        compute="_compute_partner_address_values",
        readonly=False,
        store=True,
    )

    house_type = fields.Selection(
        string="House Type",
        selection=[
            ("house", "House"),
            ("building", "Building"),
            ("residence", "Residence"),
        ],
        compute="_compute_partner_address_values",
        readonly=False,
        store=True,
    )

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        res = super()._prepare_customer_values(partner_name, is_company, parent_id)

        res["house_type"] = self.house_type
        res["residence_name"] = self.residence_name
        res["residence_number"] = self.residence_number
        res["appartment_number"] = self.appartment_number
        res["floor_number"] = self.floor_number
        res["portal_code"] = self.portal_code
        res["entry_code"] = self.entry_code

        return res
