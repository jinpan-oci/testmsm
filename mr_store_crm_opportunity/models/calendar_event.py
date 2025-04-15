from odoo import _, models


class CalendarEvent(models.Model):

    _inherit = "calendar.event"

    def default_get(self, fields):
        defaults = super().default_get(fields)

        opportunity = self.env["crm.lead"].browse(self.env.context.get("default_opportunity_id"))

        if not opportunity:
            if self.env.context.get("default_res_model") == "crm.lead":
                opportunity = self.env["crm.lead"].browse(self.env.context.get("default_res_id"))

        partner = opportunity.partner_id

        if not self.categ_ids and self.env.context.get("default_categ"):
            event = self.env["calendar.event.type"].search([("name", "=", self.env.context.get("default_categ"))])
            if event:
                self.write({"categ_ids": [(4, event.id)]})
            else:
                self.env["calendar.event.type"].create({"name": self.env.context.get("default_categ")})
                event = self.env["calendar.event.type"].search([("name", "=", self.env.context.get("default_categ"))])
                self.write({"categ_ids": [(4, event.id)]})

        if not self.location and self.env.context.get("default_location"):
            defaults["location"] = self.env.context.get("default_location")

        if not self.description and partner:
            description = opportunity.name + "\n" if opportunity.name else ""
            description += partner.name + "\n"
            description += _("Mobile : ") + (partner.mobile or opportunity.mobile) + "\n" if partner.mobile or opportunity.mobile else ""
            description += _("Phone : ") + (partner.phone or opportunity.phone) + "\n" if partner.phone or opportunity.phone else ""
            description += _("Email : ") + (partner.email or opportunity.email_from) + "\n" if partner.email or opportunity.email_from else ""

            if partner.street or opportunity.street:
                if partner.street:
                    if partner.street2:
                        description += _("Address : ") + partner.street + ", " + partner.street2 + "\n"
                    else:
                        description += _("Address : ") + partner.street + "\n"
                elif opportunity.street:
                    if opportunity.street2:
                        description += _("Address : ") + opportunity.street + ", " + opportunity.street2 + "\n"
                    else:
                        description += _("Address : ") + opportunity.street + "\n"
            description += _("Zip : ") + (partner.zip or opportunity.zip) + "\n" if partner.zip or opportunity.zip else ""
            description += _("City : ") + (partner.city or opportunity.city) + "\n" if partner.city or opportunity.city else ""

            if partner.house_type or opportunity.house_type:
                if partner.house_type:
                    if partner.house_type == "residence":
                        description += _("Residence : ") + partner.residence_name + "\n" if partner.residence_name else ""
                        description += _("Residence No : ") + partner.residence_number + "\n" if partner.residence_number else ""
                        description += _("floor : ") + partner.floor_number + "\n" if partner.floor_number else ""
                        description += _("appartment : ") + partner.appartment_number + "\n" if partner.appartment_number else ""
                        description += _("portal code : ") + partner.portal_code + "\n" if partner.portal_code else ""
                        description += _("Door code : ") + partner.entry_code + "\n" if partner.entry_code else ""
                    elif partner.house_type == "building":
                        description += _("Building : ") + "\n"
                        description += _("floor : ") + partner.floor_number + "\n" if partner.floor_number else ""
                        description += _("appartment : ") + partner.appartment_number + "\n" if partner.appartment_number else ""
                        description += _("portal code : ") + partner.portal_code + "\n" if partner.portal_code else ""
                        description += _("Door code : ") + partner.entry_code + "\n" if partner.entry_code else ""
                    elif partner.house_type == "house":
                        description += _("House : ") + "\n"
                        description += _("portal code : ") + partner.portal_code + "\n" if partner.portal_code else ""
                        description += _("Door code : ") + partner.entry_code + "\n" if partner.entry_code else ""

                elif opportunity.house_type:
                    if opportunity.house_type == "residence":
                        description += _("Residence : ") + opportunity.residence_name + "\n" if opportunity.residence_name else ""
                        description += _("Residence No : ") + opportunity.residence_number + "\n" if opportunity.residence_number else ""
                        description += _("floor : ") + opportunity.floor_number + "\n" if opportunity.floor_number else ""
                        description += _("appartment : ") + opportunity.appartment_number + "\n" if opportunity.appartment_number else ""
                        description += _("portal code : ") + opportunity.portal_code + "\n" if opportunity.portal_code else ""
                        description += _("Door code : ") + opportunity.entry_code + "\n" if opportunity.entry_code else ""
                    elif opportunity.house_type == "building":
                        description += _("Building : ") + "\n"
                        description += _("floor : ") + opportunity.floor_number + "\n" if opportunity.floor_number else ""
                        description += _("appartment : ") + opportunity.appartment_number + "\n" if opportunity.appartment_number else ""
                        description += _("portal code : ") + opportunity.portal_code + "\n" if opportunity.portal_code else ""
                        description += _("Door code : ") + opportunity.entry_code + "\n" if opportunity.entry_code else ""
                    elif opportunity.house_type == "house":
                        description += _("House : ") + "\n"
                        description += _("portal code : ") + opportunity.portal_code + "\n" if opportunity.portal_code else ""
                        description += _("Door code : ") + opportunity.entry_code + "\n" if opportunity.entry_code else ""

            defaults["description"] = description
        return defaults

    def action_sale_quotations_new(self):
        if not self.opportunity_id.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")
        else:
            return self.action_new_quotation()

    def action_new_quotation(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
        action["context"] = self._prepare_opportunity_quotation_context()
        action["context"]["search_default_opportunity_id"] = self.opportunity_id.id
        action["context"]["active_test"] = True
        return action

    def _prepare_opportunity_quotation_context(self):
        """Prepares the context for a new quotation (sale.order) by sharing the values of common fields"""
        self.ensure_one()
        quotation_context = {
            "default_opportunity_id": self.opportunity_id.id,
            "default_partner_id": self.opportunity_id.partner_id.id,
            "default_campaign_id": self.opportunity_id.campaign_id.id,
            "default_medium_id": self.opportunity_id.medium_id.id,
            "default_origin": self.opportunity_id.name,
            "default_source_id": self.opportunity_id.source_id.id,
            "default_company_id": self.opportunity_id.company_id.id or self.opportunity_id.env.company.id,
            "default_tag_ids": [(6, 0, self.opportunity_id.tag_ids.ids)],
        }
        if self.opportunity_id.team_id:
            quotation_context["default_team_id"] = self.opportunity_id.team_id.id
        if self.opportunity_id.user_id:
            quotation_context["default_user_id"] = self.opportunity_id.user_id.id
        return quotation_context
