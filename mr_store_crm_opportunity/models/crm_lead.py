from odoo import _, models


class Lead(models.Model):

    _inherit = "crm.lead"

    def action_schedule_meeting(self, smart_calendar=True):
        """Open meeting's calendar view to schedule meeting on current opportunity.

        :param smart_calendar: boolean, to set to False if the view should not try to choose relevant
            mode and initial date for calendar view, see ``_get_opportunity_meeting_view_parameters``
        :return dict: dictionary value for created Meeting view
        """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("calendar.action_calendar_event")
        partner_ids = self.env.user.partner_id.ids
        if not self.partner_id:
            partner = self._find_matching_partner(email_only=True)
            if partner:
                self._handle_partner_assignment(force_partner_id=partner.id, create_missing=False)
            else:
                self._handle_partner_assignment(create_missing=True)

        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        current_opportunity_id = self.id if self.type == "opportunity" else False

        location = ""

        if self.partner_id.street:
            location = self.partner_id.street
            if self.partner_id.street2:
                location += ", " + self.partner_id.street2
            if self.partner_id.zip:
                location += ", " + self.partner_id.zip
            if self.partner_id.city:
                location += " " + self.partner_id.city
        elif self.street:
            location = self.street
            if self.street2:
                location += ", " + self.street2
            if self.zip:
                location += ", " + self.zip
            if self.city:
                location += " " + self.city

        action["context"] = {
            "search_default_opportunity_id": None,  # current_opportunity_id
            "default_opportunity_id": current_opportunity_id,
            "default_partner_id": self.partner_id.id,
            "default_partner_ids": partner_ids,
            "default_team_id": self.team_id.id,
            "default_name": self.name,
            "default_location": location or "",
            "default_categ": _("Meeting at Home"),
        }

        # 'Smart' calendar view : get the most relevant time period to display to the user.
        if current_opportunity_id and smart_calendar:
            mode, initial_date = self._get_opportunity_meeting_view_parameters()
            action["context"].update({"default_mode": mode, "initial_date": initial_date})

        return action

    def action_create_meet_at_store(self):
        action = self.action_schedule_meeting()

        if self.company_id:
            location = self.company_id.name + ", "
            location += self.company_id.street + ", " if self.company_id.street else ""
            location += self.company_id.zip + ", " if self.company_id.zip else ""
            location += self.company_id.city if self.company_id.city else ""

        action["context"]["default_location"] = location
        action["context"]["default_categ"] = _("Meeting at Store")
        return action

    def action_create_phone_meet(self):
        action = self.action_schedule_meeting()
        if self.partner_id and self.partner_id.mobile:
            action["context"]["default_location"] = "Mobile: " + self.partner_id.mobile
        elif self.partner_id and self.partner_id.phone:
            action["context"]["default_location"] = "Phone: " + self.partner_id.phone
        else:
            action["context"]["default_location"] = ""
        action["context"]["default_categ"] = _("Phone Call")
        return action

    def action_sale_quotations_new(self):

        if not self.partner_id:
            partner = self._find_matching_partner(email_only=True)
            if partner:
                self._handle_partner_assignment(force_partner_id=partner.id, create_missing=False)
            else:
                self._handle_partner_assignment(create_missing=True)

        return super().action_sale_quotations_new()
