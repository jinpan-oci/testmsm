import base64
import logging

import requests
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    _inherit = "sale.order"

    commercial_note = fields.Text(string="Commercial Note", required=False)
    map_url_1 = fields.Char(string="Map URL 1", compute="_compute_map_url_1", store=False)
    map_url_2 = fields.Char(string="Map URL 2", compute="_compute_map_url_2", store=False)
    map_url_3 = fields.Char(string="Map URL 3", compute="_compute_map_url_3", store=False)
    map_url_4 = fields.Char(string="Map URL 4", compute="_compute_map_url_4", store=False)
    map_img_1 = fields.Binary(string="Map Image 1", compute="_compute_map_img_1", store=False)
    map_img_2 = fields.Binary(string="Map Image 2", compute="_compute_map_img_2", store=False)
    map_img_3 = fields.Binary(string="Map Image 3", compute="_compute_map_img_3", store=False)
    map_img_4 = fields.Binary(string="Map Image 4", compute="_compute_map_img_4", store=False)
    map_full_address = fields.Char(string="Full Address", compute="_compute_map_full_address", store=False)

    # |To Change| type checkbox

    is_disassembly_required = fields.Boolean(string="Disassembly", default=True, required=False)
    work_deadline = fields.Char(string="Work Deadline", required=False)
    installation_note = fields.Text(string="Installation Note", required=False)
    installation_height = fields.Char(string="Installation Height", required=False)

    # storage places

    locker_canvas = fields.Char(string="Canvas Locker", default=False)
    locker_frame = fields.Char(string="Frame Locker", default=False)

    # display name

    display_name = fields.Char(string="Display Name", compute="_compute_display_name", store=False)

    # attachment

    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        string="Attachment",
        domain=[("photo_use_type", "!=", "other")],
    )
    secondary_attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        string="Secondary Attachment",
        domain=[("photo_use_type", "=", "other")],
    )

    # report line drawing (Qweb)

    line_drawing_selection = fields.Selection(
        selection=[
            ("no", "No"),
            ("y_in", "Yes Inside"),
            ("y_out", "Yes Outside"),
            ("y_exist", "Yes Existing"),
        ],
        string="Line Drawing",
        default="no",
    )

    # inherit action_confirm sale order

    def action_confirm(self):
        for order in self:
            pdf_folder = order.env["ir.actions.report"]._render_qweb_pdf("mr_store_report_folder.report_folder_raw", order.id)
            folder_data = base64.b64encode(pdf_folder[0])
            folder_values = {
                "name": _("Folder - Order n°{0} - Client {1}").format(order.id, order.partner_id.name),
                "type": "binary",
                "datas": folder_data,
                "store_fname": folder_data,
                "res_model": order._name,
                "res_id": order.id,
                "mimetype": "application/pdf",
            }

            order.env["ir.attachment"].sudo().search([("res_model", "=", order._name), ("res_id", "=", order.id), ("name", "=", folder_values["name"])]).unlink()

            folder_id = order.env["ir.attachment"].sudo().create(folder_values)

        res = super().action_confirm()
        return res

    # computes

    @api.depends("partner_id")
    def _compute_map_full_address(self):
        for record in self:
            full_address = []
            if record.partner_id.street:
                full_address.append(record.partner_id.street)
            if record.partner_id.street2:
                full_address.append(record.partner_id.street2)
            if record.partner_id.zip:
                full_address.append(record.partner_id.zip)
            if record.partner_id.city:
                full_address.append(record.partner_id.city)
            if record.partner_id.country_id:
                full_address.append(record.partner_id.country_id.name)
            address = "+".join(full_address)
            address = address.replace(" ", "+")
            record.update(
                {
                    "map_full_address": address,
                }
            )

    @api.depends("map_full_address")
    def _compute_map_url_1(self):
        for record in self:
            map_url = "https://maps.googleapis.com/maps/api/"
            map_url += "streetview?"
            map_url += "&size=400x300"
            map_url += "&location=" + record.map_full_address
            if record.env["ir.config_parameter"].sudo().get_param("google_api_key"):
                map_url += "&key=" + record.env["ir.config_parameter"].sudo().get_param("google_api_key")
            record.update(
                {
                    "map_url_1": map_url,
                }
            )

    @api.depends("map_full_address")
    def _compute_map_url_2(self):
        for record in self:
            map_url = "https://maps.googleapis.com/maps/api/"
            map_url += "staticmap?markers=size:mid%7Ccolor:red%7C"
            map_url += record.map_full_address
            map_url += "&zoom=18"
            map_url += "&maptype=hybrid"
            map_url += "&size=400x300"
            if self.env["ir.config_parameter"].sudo().get_param("google_api_key"):
                map_url += "&key=" + self.env["ir.config_parameter"].sudo().get_param("google_api_key")
            record.update(
                {
                    "map_url_2": map_url,
                }
            )

    @api.depends("map_full_address")
    def _compute_map_url_3(self):
        for record in self:
            map_url = "https://maps.googleapis.com/maps/api/"
            map_url += "staticmap?markers=size:mid%7Ccolor:red%7C"
            map_url += record.map_full_address
            map_url += "&zoom=14"
            map_url += "&maptype=hybrid"
            map_url += "&size=1200x300"
            if self.env["ir.config_parameter"].sudo().get_param("google_api_key"):
                map_url += "&key=" + self.env["ir.config_parameter"].sudo().get_param("google_api_key")
            record.update(
                {
                    "map_url_3": map_url,
                }
            )

    @api.depends("map_full_address")
    def _compute_map_url_4(self):
        for record in self:
            map_url = "https://maps.googleapis.com/maps/api/"
            map_url += "staticmap?markers=size:mid%7Ccolor:red%7C"
            map_url += record.map_full_address
            map_url += "&zoom=14"
            map_url += "&size=1200x300"
            if self.env["ir.config_parameter"].sudo().get_param("google_api_key"):
                map_url += "&key=" + self.env["ir.config_parameter"].sudo().get_param("google_api_key")
            record.update(
                {
                    "map_url_4": map_url,
                }
            )

    def get_image_from_url(self, url):
        data = ""
        try:
            data = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")
        except Exception as e:
            _logger.warning("Can't load the image from URL %s" % url)
            logging.exception(e)
        return data

    @api.depends("map_url_1")
    def _compute_map_img_1(self):
        for record in self:
            image = None
            if record.map_url_1:
                image = self.get_image_from_url(record.map_url_1)
            record.update(
                {
                    "map_img_1": image,
                }
            )

    @api.depends("map_url_2")
    def _compute_map_img_2(self):
        for record in self:
            image = None
            if record.map_url_2:
                image = self.get_image_from_url(record.map_url_2)
            record.update(
                {
                    "map_img_2": image,
                }
            )

    @api.depends("map_url_3")
    def _compute_map_img_3(self):
        for record in self:
            image = None
            if record.map_url_3:
                image = self.get_image_from_url(record.map_url_3)
            record.update(
                {
                    "map_img_3": image,
                }
            )

    @api.depends("map_url_4")
    def _compute_map_img_4(self):
        for record in self:
            image = None
            if record.map_url_4:
                image = self.get_image_from_url(record.map_url_4)
            record.update(
                {
                    "map_img_4": image,
                }
            )

    @api.depends("name", "partner_id", "order_line")
    def _compute_display_name(self):
        for record in self:
            if record.name and record.partner_id and record.order_line:
                display_name = [record.name, record.partner_id.name]
                separator = " - "
                if record.order_line:
                    for line in record.order_line:
                        if line.product_template_id.type == "product":
                            display_name.append(str(line.product_uom_qty) + " x " + line.product_template_id.name)
                            break
                record.update(
                    {
                        "display_name": separator.join(display_name),
                    }
                )
            else:
                record.update({"display_name": ""})

    def action_create_attachment(self):
        return self.env["ir.actions.act_window"]._for_xml_id("mr_store_report_folder.action_attachment_add_view")

    # ----------------------------------------------------------------------------------------------------------------------------
    # OLD - DO NOT USE FROM NOW ON - ONLY FOR USE WITH MIGRATION SCRIPTS ---------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------

    security_harness = fields.Boolean(string="Harness", default=False)
    security_anchor_bar = fields.Boolean(string="Anchor Bar", default=False)
    security_other = fields.Char(string="Other", default=False)

    line_no = fields.Boolean(string="No", default=False)
    line_yes_interior = fields.Boolean(string="Yes, Indoor", default=False)
    line_yes_exterior = fields.Boolean(string="Yes, Outdoor", default=False)
    line_existing = fields.Boolean(string="Existing", default=False)
    line_other = fields.Char(string="Other Line Drawing", required=False)

    stool_3_steps = fields.Boolean(string="3 Steps - 2.66m", default=False)
    stool_4_steps = fields.Boolean(string="4 Steps - 2.88m", default=False)
    stool_5_steps = fields.Boolean(string="5 Steps - 3.10m", default=False)
    stool_6_steps = fields.Boolean(string="6 Steps - 3.32m", default=False)
    stool_7_steps = fields.Boolean(string="7 Steps - 3.54m", default=False)
    stool_8_steps = fields.Boolean(string="8 Steps - 3.76m", default=False)
    stool_9_steps = fields.Boolean(string="9 Steps - 3.98m", default=False)
    stool_10_steps = fields.Boolean(string="10 Steps - 4.20m", default=False)

    ladder_2_sections = fields.Boolean(string="2 Sections - 4.20m", default=False)
    ladder_3_sections = fields.Boolean(string="3 Sections - 6.30m", default=False)
    ladder_firefighter = fields.Boolean(string="Firefighter - 8.30m", default=False)
    ladder_retractable = fields.Boolean(string="Retractable - 8.30m", default=False)
    ladder_foldable = fields.Boolean(string="Foldable - 8.30m", default=False)

    basket_scaffodable = fields.Boolean(string="Scaffodable", default=False)
    basket_vl_12m = fields.Boolean(string="Basket VL 12m", default=False)
    basket_vl_16m = fields.Boolean(string="Basket VL 16m", default=False)
    basket_scissors_16m = fields.Boolean(string="Basket Scissors 16m", default=False)
    basket_scissors_20m = fields.Boolean(string="Basket Scissors 20m", default=False)
    basket_auto_12m = fields.Boolean(string="Basket Auto 12m", default=False)
    basket_auto_15m = fields.Boolean(string="Basket Auto 15m", default=False)
    basket_other = fields.Char(string="Other Basket Height", required=False)

    wall_concrete = fields.Boolean(string="Concrete", default=False)
    wall_hollow = fields.Boolean(string="Hollow", default=False)
    wall_placo = fields.Boolean(string="Placo", default=False)
    wall_aluminum = fields.Boolean(string="Aluminum", default=False)
    wall_wood = fields.Boolean(string="Wood", default=False)
    wall_grumble_stone = fields.Boolean(string="Grumble Stone", default=False)
    wall_exterior_insulation = fields.Boolean(string="Exterior Insulation", default=False)
    wall_other = fields.Char(string="Other Wall Type", required=False)

    protection_cardboard = fields.Boolean(string="Cardboard", default=False)
    protection_mr_store_carpet = fields.Boolean(string="MR Store Carpet", default=False)
    protection_ribbon = fields.Boolean(string="Ribbon", default=False)
    protection_board = fields.Boolean(string="Board", default=False)
    protection_barrier = fields.Boolean(string="Barrier", default=False)
    protection_other = fields.Char(string="Other Protection Type", required=False)

    forwarding_ropes = fields.Boolean(string="Ropes", default=False)
    forwarding_lifting_kit = fields.Boolean(string="Lifting Kit", default=False)
    forwarding_shark_4 = fields.Boolean(string="Shark 4", default=False)
    forwarding_shark_5 = fields.Boolean(string="Shark 5", default=False)
    forwarding_shark_6 = fields.Boolean(string="Shark 6", default=False)
    forwarding_other = fields.Char(string="Other Forwarding Type", required=False)

    silicon_transparent = fields.Boolean(string="Silicon - Transparent", default=False)
    silicon_white = fields.Boolean(string="Silicon - White", default=False)
    silicon_ivory = fields.Boolean(string="Silicon - Ivory", default=False)
    silicon_black = fields.Boolean(string="Silicon - Black", default=False)
    silicon_brown = fields.Boolean(string="Silicon - Brown", default=False)
    silicon_grey = fields.Boolean(string="Silicon - Grey", default=False)
    silicon_anthracite = fields.Boolean(string="Silicon - Anthracite", default=False)
    silicon_other = fields.Char(string="Other Silicon Type", required=False)

    glue_pergola_glue = fields.Boolean(string="Pergola Glue", default=False)
    glue_glue_gun = fields.Boolean(string="Glue Gun", default=False)
    glue_other = fields.Char(string="Other Glue Type", required=False)

    spray_aluminum_cleaner = fields.Boolean(string="Aluminum Cleaner", default=False)
    spray_penetrating = fields.Boolean(string="Penetrating", default=False)
    spray_silicon_lubricant = fields.Boolean(string="Silicon Lubricant", default=False)
    spray_other = fields.Char(string="Other Spray Type", required=False)

    paint_white = fields.Boolean(string="Paint - White", default=False)
    paint_ivory = fields.Boolean(string="Paint - Ivory", default=False)
    paint_black = fields.Boolean(string="Paint - Black", default=False)
    paint_grey = fields.Boolean(string="Paint - Grey", default=False)
    paint_brown = fields.Boolean(string="Paint - Brown", default=False)
    paint_anthracite = fields.Boolean(string="Paint - Anthracite", default=False)
    paint_other = fields.Char(string="Other Paint Type", required=False)

    lifting_tool_1_elevator_3m = fields.Boolean(string="1 Elevator 3M", default=False)
    lifting_tool_2_elevator_3m = fields.Boolean(string="2 Elevator 3M", default=False)
    lifting_tool_1_elevator_38m = fields.Boolean(string="1 Elevator 3.8M", default=False)
    lifting_tool_2_elevator_38m = fields.Boolean(string="2 Elevator 3.8M", default=False)
    lifting_tool_1_manual_elevator_3m = fields.Boolean(string="1 Manual Elevator 3M", default=False)

    tool_silicon_pump_18v = fields.Boolean(string="Silicon Pump 18V", default=False)
    tool_suction_cup = fields.Boolean(string="Suction Cup", default=False)
    tool_edger_220v = fields.Boolean(string="Edger 220V", default=False)
    tool_long_drill_bit = fields.Boolean(string="Long Drill Bit", default=False)
    tool_laser = fields.Boolean(string="Laser", default=False)
    tool_riveter = fields.Boolean(string="Riveter", default=False)
    tool_big_angle_grinder_220v = fields.Boolean(string="Big Angle Grinder 220V", default=False)

    saw_jigsaw = fields.Boolean(string="Jigsaw", default=False)
    saw_milter_saw = fields.Boolean(string="Milter Saw", default=False)
    saw_saber_220v = fields.Boolean(string="Saber 220V", default=False)
    saw_saber_18v = fields.Boolean(string="Saber 18V", default=False)
    saw_wood_circular = fields.Boolean(string="Wood Circular Saw", default=False)

    masonry_ruler_4m = fields.Boolean(string="Ruler 4M", default=False)
    masonry_ruler_5m = fields.Boolean(string="Ruler 5M", default=False)
    masonry_ruler_6m = fields.Boolean(string="Ruler 6M", default=False)
    masonry_other = fields.Char(string="Other Masonry Tool", required=False)

    kit_iron_drill_bit = fields.Boolean(string="Iron Drill Bit Kit", default=False)
    kit_pergola = fields.Boolean(string="Pergola Kit", default=False)
    kit_quiberon = fields.Boolean(string="Quiberon Kit", default=False)
    kit_metal_curtain = fields.Boolean(string="Metal Curtain Kit", default=False)
    kit_carpentry = fields.Boolean(string="Carpentry Kit", default=False)
    kit_traditionnal_roller_shutter = fields.Boolean(string="Traditionnal Roller Shutter Kit", default=False)
    kit_monobloc_roller_shutter = fields.Boolean(string="Monobloc Roller Shutter Kit", default=False)
    kit_bayblock_roller_shutter = fields.Boolean(string="Bayblock Roller Shutter Kit", default=False)
    kit_led = fields.Boolean(string="LED Kit", default=False)
    kit_manual_velum = fields.Boolean(string="Manual Velum Kit", default=False)
    kit_belt_velum = fields.Boolean(string="Belt Velum Kit", default=False)
    kit_cable_velum = fields.Boolean(string="Cable Velum Kit", default=False)
    kit_corded_grinder = fields.Boolean(string="Corded Grinder Kit", default=False)
    kit_stapler = fields.Boolean(string="Stapler Kit", default=False)
    kit_rings = fields.Boolean(string="Rings Kit", default=False)
    kit_hole_saw = fields.Boolean(string="Hole Saw Kit", default=False)
