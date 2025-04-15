import base64

import requests
from odoo import _, fields, models

# from trello import TrelloClient
from odoo.addons.mr_store_trello_connector.trello.trelloclient import (
    TrelloClient as TrelloClient,
)


class TrelloSync(models.Model):
    _name = "trello.sync"
    _description = "Trello base connector"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Is Cron Active", default=True)

    board = fields.Char(string="Select Board", required=False, store=True)
    push_list = fields.Char(string="Push List", required=False, store=True)
    pull_list = fields.Char(string="Pull List", required=False, store=True)

    available_boards = fields.Char(string="Available Boards", compute="_compute_available_boards", store=False)
    available_push_lists = fields.Char(
        string="Available Lists - push",
        compute="_compute_available_push_lists",
        store=False,
    )
    available_pull_lists = fields.Char(
        string="Available Lists - pull",
        compute="_compute_available_pull_lists",
        store=False,
    )

    def _compute_available_boards(self):
        for record in self:
            client = record.get_instance()
            boards = client.list_boards()
            available_boards = ""
            if boards:
                for board in boards:
                    available_boards += "'" + board.name + "' "
                record.available_boards = available_boards
            else:
                record.available_boards = "No boards available, check API and Token Keys"

    def _compute_available_push_lists(self):
        for record in self:
            client = record.get_instance()
            boards = client.list_boards()
            record.available_push_lists = ""
            if record.board:
                for board in boards:
                    if board.name == record.board:
                        board_lists = board.all_lists()
                        available_push_lists = ""
                        for board_list in board_lists:
                            available_push_lists += "'" + board_list.name + "' "
                        record.available_push_lists = available_push_lists
            else:
                record.available_push_lists = "No board selected, or refresh page"

    def _compute_available_pull_lists(self):
        for record in self:
            record.available_pull_lists = ""
            client = record.get_instance()
            boards = client.list_boards()
            if record.board:
                for board in boards:
                    if board.name == record.board:
                        board_lists = board.all_lists()
                        available_pull_lists = ""
                        for board_list in board_lists:
                            available_pull_lists += "'" + board_list.name + "' "
                        record.available_pull_lists = available_pull_lists
            else:
                record.available_pull_lists = "No board selected, or refresh page"

    def _compute_file_datas(self, url):
        for record in self:
            key = record.env["ir.config_parameter"].sudo().get_param("trello_api_key")
            token = record.env["ir.config_parameter"].sudo().get_param("trello_token")
            headers = {"Authorization": f"OAuth oauth_consumer_key={key!r}, oauth_token={token!r}"}
            pdf_file = requests.get(url, headers=headers)
            return base64.b64encode(pdf_file.content).replace(b"\n", b"")

    def get_instance(self):
        return TrelloClient(
            api_key=self.env["ir.config_parameter"].sudo().get_param("trello_api_key"),
            api_secret=self.env["ir.config_parameter"].sudo().get_param("trello_api_secret"),
            token=self.env["ir.config_parameter"].sudo().get_param("trello_token"),
            token_secret=self.env["ir.config_parameter"].sudo().get_param("trello_token_secret"),
        )

    def get_actual_board(self):
        return self.get_board(self.env["trello.sync"].search([])[0].board)

    def get_board(self, push_pull_board):
        client = self.get_instance()
        boards = client.list_boards()
        for board in boards:
            if board.name == push_pull_board:
                return board

    def get_boards(self):
        client = self.get_instance()
        return client.list_boards()

    def get_list(self, board, push_pull_list):
        board_lists = board.all_lists()
        for board_list in board_lists:
            if board_list.name == push_pull_list:
                return board_list
        return False

    def push(self):
        tasks_to_treat = self.env["project.task"].sudo().search([("trello_idcardsource", "=", False), ("sale_order_id", "!=", False)])
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for task in tasks_to_treat:

            name = task.sale_order_id.name + " - " + task.partner_id.name + ":  " + task.sale_order_id.order_line[0].product_id.name
            desc = task.description + "\n" if task.description else ""
            desc += base_url + "/web#id=" + str(task.id) + "&view_type=form&model=project.task" + "\n"
            desc += task.partner_id.name + "\n" if task.partner_id.name else ""
            desc += task.partner_id.email + "\n" if task.partner_id.email else ""
            desc += task.partner_id.phone + "\n" if task.partner_id.phone else ""
            desc += task.partner_id.mobile + "\n" if task.partner_id.mobile else ""
            desc += task.partner_id.contact_address_complete + "\n" if task.partner_id.contact_address_complete else ""
            desc += "Order: \n"
            for line in task.sale_order_id.order_line:
                desc += "- " + line.name + "\n"

            address = task.partner_id.contact_address_complete if task.partner_id.contact_address_complete else None

            card = self.set_card_to_plannify(name, desc, address, task)
            task.trello_idcardsource = card.id
            task.trello_url = f"<a href={card.url!r}>Carte Planning</a>"

        return True

    def test_push(self):
        self.push()

    def push_one(self, record):
        tasks_to_treat = [task for task in record.tasks_ids]
        use_only_first_task = self.env["ir.config_parameter"].sudo().get_param("use_only_first_task")
        if use_only_first_task and tasks_to_treat:
            tasks_to_treat = [tasks_to_treat[0]]
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for task in tasks_to_treat:
            is_card_existing = True if task.trello_idcardsource else False
            if is_card_existing:
                client = self.get_instance()
                card = client.get_card(str(task.trello_idcardsource))
                if card.closed:
                    is_card_existing = False
                else:
                    attachments = card.get_attachments()
                    is_folder = False
                    is_order = False

                    if attachments:
                        for attachment in attachments:
                            if attachment.name.find(_("Folder Order")) != -1:
                                is_folder = True
                                card.remove_attachment(attachment.id)

                                pdf_folder = (
                                    task.env["ir.actions.report"]
                                    .sudo()
                                    ._render_qweb_pdf(
                                        "mr_store_report_folder.action_report_folder_raw",
                                        [task.sale_order_id.id],
                                    )
                                )
                                card.attach(
                                    _("Folder Order ") + task.sale_order_id.name + ".pdf",
                                    "application/pdf",
                                    pdf_folder[0],
                                    None,
                                    "true",
                                )

                            elif attachment.name.find(_("Order")) != -1:
                                is_order = True
                                card.remove_attachment(attachment.id)

                                pdf_saleorder = (
                                    task.env["ir.actions.report"]
                                    .sudo()
                                    ._render_qweb_pdf(
                                        "sale.action_report_saleorder",
                                        [task.sale_order_id.id],
                                    )
                                )
                                card.attach(
                                    _("Order ") + task.sale_order_id.name + ".pdf",
                                    "application/pdf",
                                    pdf_saleorder[0],
                                    None,
                                    "true",
                                )

                    if not attachments or not is_folder:
                        pdf_folder = (
                            task.env["ir.actions.report"]
                            .sudo()
                            ._render_qweb_pdf(
                                "mr_store_report_folder.action_report_folder_raw",
                                [task.sale_order_id.id],
                            )
                        )
                        card.attach(
                            _("Folder Order ") + task.sale_order_id.name + ".pdf",
                            "application/pdf",
                            pdf_folder[0],
                            None,
                            "true",
                        )

                    if not attachments or not is_order:
                        pdf_saleorder = task.env["ir.actions.report"].sudo()._render_qweb_pdf("sale.action_report_saleorder", [task.sale_order_id.id])
                        card.attach(
                            _("Order ") + task.sale_order_id.name + ".pdf",
                            "application/pdf",
                            pdf_saleorder[0],
                            None,
                            "true",
                        )

                    card.subscribe()

            if not is_card_existing:
                order_id = task.sale_order_id
                name = order_id.display_name if order_id.display_name else ""

                desc = "OC: " + order_id.display_name + "\n\n" if order_id.display_name else ""
                desc += ":construction: " + _("[Odoo Task URL]") + "('" + base_url + "/web#id=" + str(task.id) + "&view_type=form&model=project.task')" + "\n\n"
                desc += "URL: " + base_url + "/web#id=" + str(task.id) + "&view_type=form&model=project.task" + "\n\n"
                desc += ":construction_worker: " + _("Installation Note: ") + order_id.installation_note + "\n\n" if order_id.installation_note else ""
                desc += _("P - Installer Number: ") + str(task.trello_installers_number) + "\n" if task.trello_installers_number else ""
                desc += _("H - Duration: ") + str(task.trello_duration) + "\n" if task.trello_duration else ""
                desc += _("AP - Pax Number for Forwarding: ") + str(task.trello_pax_number_for_forwarding) + "\n" if task.trello_pax_number_for_forwarding else ""
                desc += _("AH - Forwarding Duration: ") + str(task.trello_forwarding_duration) + "\n" if task.trello_forwarding_duration else ""
                desc += ":date: " + _("Command Date: ") + str(order_id.date_order) + "\n\n" if order_id.date_order else ""
                desc += ":date: " + _("Create Date: ") + str(order_id.create_date) + "\n\n" if order_id.create_date else ""
                desc += ":hourglass: " + _("Work Deadline: ") + str(order_id.work_deadline) + "\n\n" if order_id.work_deadline else ""
                desc += ":credit_card: " + _("Payment Terms: ") + str(order_id.payment_term_id.name) + "\n\n" if order_id.payment_term_id.name else ""
                desc += (
                    ":moneybag: " + _("Deposit: ") + str(order_id.amount_total - order_id.amount_to_invoice) + "\n\n"
                    if order_id.amount_to_invoice and order_id.amount_total
                    else ""
                )
                desc += ":man: " + _("Commercial note: ") + order_id.commercial_note + "\n\n" if order_id.commercial_note else ""
                desc += ":bust_in_silhouette: " + "Contact: " + "\n"
                desc += ":iphone: " + _("Mobile: ") + task.partner_id.mobile + "\n" if task.partner_id.mobile else ""
                desc += ":telephone: " + _("Phone: ") + task.partner_id.phone + "\n" if task.partner_id.phone else ""
                desc += ":mailbox_with_mail: " + _("Email: ") + task.partner_id.email + "\n\n" if task.partner_id.email else ""
                desc += ":house: " + _("Install Address: ") + "\n"
                desc += order_id.partner_shipping_id.street + ", " if order_id.partner_shipping_id.street else ""
                desc += order_id.partner_shipping_id.street2 + ", " if order_id.partner_shipping_id.street2 else ""
                desc += order_id.partner_shipping_id.zip + ", " if order_id.partner_shipping_id.zip else ""
                desc += order_id.partner_shipping_id.city + "\n" if order_id.partner_shipping_id.city else ""
                if order_id.partner_shipping_id.house_type == "residence":
                    desc += _("Residence: ") + order_id.partner_shipping_id.residence_name + "\n" if order_id.partner_shipping_id.residence_name else ""
                    desc += _("Residence No: ") + order_id.partner_shipping_id.residence_number + "\n" if order_id.partner_shipping_id.residence_number else ""
                    desc += _("Floor: ") + order_id.partner_shipping_id.floor_number + "\n" if order_id.partner_shipping_id.floor_number else ""
                    desc += _("Appartment: ") + order_id.partner_shipping_id.appartment_number + "\n" if order_id.partner_shipping_id.appartment_number else ""
                    desc += _("Portal Code: ") + order_id.partner_shipping_id.portal_code + "\n" if order_id.partner_shipping_id.portal_code else ""
                    desc += _("Door Code: ") + order_id.partner_shipping_id.entry_code + "\n\n" if order_id.partner_shipping_id.entry_code else ""
                elif order_id.partner_shipping_id.house_type == "building":
                    desc += _("Building: ") + "\n"
                    desc += _("Floor: ") + order_id.partner_shipping_id.floor_number + "\n" if order_id.partner_shipping_id.floor_number else ""
                    desc += _("Appartment: ") + order_id.partner_shipping_id.appartment_number + "\n" if order_id.partner_shipping_id.appartment_number else ""
                    desc += _("Portal Code: ") + order_id.partner_shipping_id.portal_code + "\n" if order_id.partner_shipping_id.portal_code else ""
                    desc += _("Door Code: ") + order_id.partner_shipping_id.entry_code + "\n\n" if order_id.partner_shipping_id.entry_code else ""
                elif order_id.partner_shipping_id.house_type == "house":
                    desc += _("House: ") + "\n"
                    desc += _("Portal Code: ") + order_id.partner_shipping_id.portal_code + "\n" if order_id.partner_shipping_id.portal_code else ""
                    desc += _("Door Code: ") + order_id.partner_shipping_id.entry_code + "\n\n" if order_id.partner_shipping_id.entry_code else ""
                desc += ":office: " + _("Billing Address: ") + "\n"
                desc += order_id.partner_invoice_id.street + ", " if order_id.partner_invoice_id.street else ""
                desc += order_id.partner_invoice_id.street2 + ", " if order_id.partner_invoice_id.street2 else ""
                desc += order_id.partner_invoice_id.zip + ", " if order_id.partner_invoice_id.zip else ""
                desc += order_id.partner_invoice_id.city + "\n\n" if order_id.partner_invoice_id.city else ""
                desc += ":package: " + _("Order: \n")
                for line in task.sale_order_id.order_line:
                    desc += "- " + line.name + "\n"

                address = task.partner_id.contact_address_complete if task.partner_id.contact_address_complete else None

                card = self.set_card_to_plannify(name, desc, address, task)
                task.trello_idcardsource = card.id
                task.trello_url = f"<a href={card.url!r}>Carte Planning</a>"

        return True

    def test_push_one(self):
        self.push_one()

    def set_card_to_plannify(self, name, desc, address, task):
        board = self.get_board(self.env["trello.sync"].search([])[0].board)
        custom_fields = board.get_custom_field_definitions()
        board.all_members()
        list_to_add = self.get_list(board, self.env["trello.sync"].search([])[0].push_list)
        locationName = task.sale_order_id.name
        coordinates = str(task.partner_id.partner_latitude) + "," + str(task.partner_id.partner_longitude)

        # add_card(self, name, desc=None, labels=None, due="null", source=None, position=None, assign=None, keep_from_source="all", url_source=None, address= None):

        card = list_to_add.add_card(
            name,
            desc,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            address,
            locationName,
            coordinates,
        )

        # import pdb
        # pdb.set_trace()

        if card:
            card.fetch()
            # for member in members:
            # card.assign(member.id)
            for custom_field in custom_fields:
                if custom_field.name == "P" and task.trello_installers_number:
                    card.set_custom_field(str(task.trello_installers_number), custom_field)
                elif custom_field.name == "AP" and task.trello_pax_number_for_forwarding:
                    card.set_custom_field(str(task.trello_pax_number_for_forwarding), custom_field)
                elif custom_field.name == "H" and task.trello_duration:
                    card.set_custom_field(str(task.trello_duration), custom_field)
                elif custom_field.name == "AH" and task.trello_forwarding_duration:
                    card.set_custom_field(str(task.trello_forwarding_duration), custom_field)
                elif custom_field.name == "L" and task.trello_L:
                    card.set_custom_field(str(task.trello_L), custom_field)
                # elif custom_field.name == 'RDV CONFIRMED':
                # card.set_custom_field("Confirmed", custom_field) if task.trello_rdv_confirmed else card.set_custom_field("Not Confirmed", custom_field)
                elif custom_field.name == "HT" and task.sale_order_id.amount_untaxed:
                    card.set_custom_field(str(task.sale_order_id.amount_untaxed), custom_field)
                elif custom_field.name == "DATE DEVIS" and task.sale_order_id.date_order:
                    card.set_custom_field(str(task.sale_order_id.date_order), custom_field)
                elif custom_field.name == "FIN TRAVAUX" and task.sale_order_id.work_deadline:
                    card.set_custom_field(str(task.sale_order_id.work_deadline), custom_field)
                # elif custom_field.name == 'Payment Terms':
                # card.set_custom_field( str(task.sale_order_id.payment_term_id.name), custom_field)
                elif custom_field.name == "ACOMPTE" and task.sale_order_id.amount_to_invoice and task.sale_order_id.amount_total:
                    card.set_custom_field(
                        str(task.sale_order_id.amount_total - task.sale_order_id.amount_to_invoice),
                        custom_field,
                    )
                elif custom_field.name == "N° COMMANDE" and task.sale_order_id.name:
                    card.set_custom_field(str(task.sale_order_id.name), custom_field)
                else:
                    pass
            if task.sale_order_id:
                if task.sale_order_id.order_line and task.sale_order_id.order_line[0].product_id and task.sale_order_id.order_line[0].product_id.image_1920:
                    if task.sale_order_id.order_line[0].product_id.image_1920:
                        encoded_image = task.sale_order_id.order_line[0].product_id.image_1920
                        binary_image = base64.b64decode(encoded_image)
                        card.attach(
                            task.sale_order_id.order_line[0].product_id.name,
                            "image/jpeg",
                            binary_image,
                            None,
                            "true",
                        )

                pdf_folder = (
                    task.env["ir.actions.report"]
                    .sudo()
                    ._render_qweb_pdf(
                        "mr_store_report_folder.action_report_folder_raw",
                        [task.sale_order_id.id],
                    )
                )
                card.attach(
                    _("Folder Order ") + task.sale_order_id.name + ".pdf",
                    "application/pdf",
                    pdf_folder[0],
                    None,
                    "true",
                )

                pdf_saleorder = task.env["ir.actions.report"].sudo()._render_qweb_pdf("sale.action_report_saleorder", [task.sale_order_id.id])
                card.attach(
                    _("Order ") + task.sale_order_id.name + ".pdf",
                    "application/pdf",
                    pdf_saleorder[0],
                    None,
                    "true",
                )

            card.subscribe()
            card.comment("To planify")

        return card

    def pull(self):
        # import pdb ; pdb.set_trace()
        board = self.get_board(self.board)
        list_to_add = self.get_list(board, self.pull_list)
        if list_to_add:
            for card in list_to_add.list_cards():
                # import pdb ; pdb.set_trace()
                # card.fetch()
                task = self.env["project.task"].sudo().search([("trello_idcardsource", "=", card.id)])
                saleorder = task.sale_order_id
                if task:
                    # task.write({'status':'card.id'})
                    # import pdb ; pdb.set_trace()
                    card.fetch(True)
                    for attachment in card.attachments:
                        if attachment["name"].find(_("Folder")) == -1 and attachment["name"].find(_("Order")) == -1:
                            if not self.env["ir.attachment"].search(
                                [
                                    ("res_model", "=", "sale.order"),
                                    ("res_id", "=", saleorder.id),
                                ]
                            ):
                                datas = self._compute_file_datas(attachment["url"])
                                self.env["ir.attachment"].create(
                                    {
                                        "name": attachment["name"],
                                        "datas": datas,
                                        "res_model": "sale.order",
                                        "res_id": saleorder.id,
                                        "type": "binary",
                                    }
                                )
                            else:
                                for saleattachment in self.env["ir.attachment"].search(
                                    [
                                        ("res_model", "=", "sale.order"),
                                        ("res_id", "=", saleorder.id),
                                    ]
                                ):
                                    if saleattachment.name != attachment["name"]:
                                        datas = self._compute_file_datas(attachment["url"])
                                        self.env["ir.attachment"].create(
                                            {
                                                "name": attachment["name"],
                                                "datas": datas,
                                                "res_model": "sale.order",
                                                "res_id": saleorder.id,
                                                "type": "binary",
                                            }
                                        )
                    for comment in card.comments:
                        self.env["mail.message"].create(
                            {
                                "subject": comment["data"]["text"],
                                "body": comment["data"]["text"],
                                "model": "project.task",
                                "res_id": task.id,
                                "message_type": "comment",
                            }
                        )
                    # create timesheet on task with users who comments the card
                    task.stage_id = self.env["project.task.type"].search([("is_trello_finished_card", "=", True)], limit=1).id
                    task.action_fsm_validate()
                    card.set_closed(True)
                else:
                    continue
            return list_to_add.list_cards()
        return True

    def test_pull(self):
        self.pull()

    def _run_cron(self):
        for record in self.search([]):
            if record.board and record.pull_list:
                record.pull()

    def prepare_cards(self, task):

        card = {
            "name": task.name,
            "desc": task.description,
            "idmembers": task.trello_idmembers,
        }
        return card

    # moulinette

    def action_moulinette(self):
        for record in self:
            for product in record.env["product.template"].search([]):
                if product.type == "product":
                    if product.x_studio_pdf and not product.presentation_before:
                        product.presentation_before = product.x_studio_pdf
                    if product.x_studio_pdf_apres and not product.presentation_after:
                        product.presentation_after = product.x_studio_pdf_apres
