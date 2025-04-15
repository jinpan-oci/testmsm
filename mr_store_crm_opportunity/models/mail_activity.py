from odoo import models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    def action_create_calendar_event(self):
        """Small override of the action that creates a calendar.

        If the activity is linked to a crm.lead through the "opportunity_id" field, we include in
        the action context the default values used when scheduling a meeting from the crm.lead form
        view.
        e.g: It will set the partner_id of the crm.lead as default attendee of the meeting.
        """

        action = super().action_create_calendar_event()

        if self.env.context.get("default_res_model") != "crm.lead":
            return action

        opportunity = self.calendar_event_id.opportunity_id or self.env["crm.lead"].browse(self.env.context.get("default_res_id"))
        if opportunity:
            if not opportunity.partner_id:
                partner = opportunity._find_matching_partner(email_only=True)
                if partner:
                    opportunity._handle_partner_assignment(force_partner_id=partner.id, create_missing=False)
                else:
                    opportunity._handle_partner_assignment(create_missing=True)
            opportunity_action_context = opportunity.action_schedule_meeting(smart_calendar=False).get("context", {})
            opportunity_action_context["initial_date"] = self.calendar_event_id.start

            action["context"].update(opportunity_action_context)
        return action
