from odoo import fields, models


class BaseInstallation(models.Model):

    _name = "base.installation"
    _description = "Base Installation"
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    base_installation_line_ids = fields.One2many("base.installation.line", "base_installation_id", string="Installation Lines")

    def apply_to_old_orders(self):
        base_installation_ids = self.env["base.installation"].search([])
        orders = self.env["sale.order"].search([("transaction_installation_ids", "=", False)])
        for order in orders:
            for base_installation in base_installation_ids:
                default_line = base_installation.base_installation_line_ids.search([("name", "=", "sans")], limit=1)
                if not default_line:
                    default_line = self.env["base.installation.line"].create(
                        {
                            "name": "sans",
                            "base_installation_id": base_installation.id,
                        }
                    )
                self.env["transaction.installation"].create(
                    {
                        "base_installation_id": base_installation.id,
                        "base_installation_line_ids": [(4, default_line.id)],
                        "sale_order_id": order.id,
                    }
                )

    def data_migration(self):
        orders = self.env["sale.order"].search([])

        for order in orders:
            if order.line_no:
                order.line_drawing_selection = "no"
            if order.line_yes_interior:
                order.line_drawing_selection = "y_in"
            if order.line_yes_exterior:
                order.line_drawing_selection = "y_out"
            if order.line_existing:
                order.line_drawing_selection = "y_exist"

            if order.security_harness or order.security_anchor_bar or order.security_other:
                installation_id = self.env["base.installation"].search([("name", "=", "Sécurité")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Sécurité"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.security_harness:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Harnais")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Harnais", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.security_anchor_bar:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Barre d'ancrage")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Barre d'ancrage", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.security_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.security_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.security_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.stool_3_steps
                or order.stool_4_steps
                or order.stool_5_steps
                or order.stool_6_steps
                or order.stool_7_steps
                or order.stool_8_steps
                or order.stool_9_steps
                or order.stool_10_steps
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Marche pied")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Marche pied"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.stool_3_steps:
                    line_id = self.env["base.installation.line"].search([("name", "=", "3 Marches - 2.66m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "3 Marches - 2.66m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.stool_4_steps:
                    line_id = self.env["base.installation.line"].search([("name", "=", "4 Marches - 2.88m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "4 Marches - 2.88m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.stool_5_steps:
                    line_id = self.env["base.installation.line"].search([("name", "=", "5 Marches - 3.10m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "5 Marches - 3.10m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.stool_6_steps:
                    line_id = self.env["base.installation.line"].search([("name", "=", "6 Marches - 3.32m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "6 Marches - 3.32m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.stool_7_steps:
                    line_id = self.env["base.installation.line"].search([("name", "=", "7 Marches - 3.54m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "7 Marches - 3.54m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.stool_8_steps:
                    line_id = self.env["base.installation.line"].search([("name", "=", "8 Marches - 3.76m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "8 Marches - 3.76m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.stool_9_steps:
                    line_id = self.env["base.installation.line"].search([("name", "=", "9 Marches - 3.98m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "9 Marches - 3.98m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.stool_10_steps:
                    line_id = self.env["base.installation.line"].search([("name", "=", "10 Marches - 4.20m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "10 Marches - 4.20m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if order.ladder_2_sections or order.ladder_3_sections or order.ladder_firefighter or order.ladder_retractable or order.ladder_foldable:
                installation_id = self.env["base.installation"].search([("name", "=", "Echelle")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Echelle"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.ladder_2_sections:
                    line_id = self.env["base.installation.line"].search([("name", "=", "2 Sections - 4.20m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "2 Sections - 4.20m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.ladder_3_sections:
                    line_id = self.env["base.installation.line"].search([("name", "=", "3 Sections - 6.30m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "3 Sections - 6.30m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.ladder_firefighter:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Pompier - 8.30m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Pompier - 8.30m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.ladder_retractable:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Rétractable - 8.30m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Rétractable - 8.30m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.ladder_foldable:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Pliable - 8.30m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Pliable - 8.30m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.basket_scaffodable
                or order.basket_vl_12m
                or order.basket_vl_16m
                or order.basket_scissors_16m
                or order.basket_scissors_20m
                or order.basket_auto_12m
                or order.basket_auto_15m
                or order.basket_other
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Nacelle")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Nacelle"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.basket_scaffodable:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Échafaudage")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Échafaudage", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.basket_vl_12m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Nacelle VL 12m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Nacelle VL 12m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.basket_vl_16m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Nacelle VL 16m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Nacelle VL 16m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.basket_scissors_16m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Nacelle Ciseaux 16m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Nacelle Ciseaux 16m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.basket_scissors_20m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Nacelle Ciseaux 20m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Nacelle Ciseaux 20m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.basket_auto_12m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Nacelle Auto 12m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Nacelle Auto 12m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.basket_auto_15m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Nacelle Auto 15m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Nacelle Auto 15m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.basket_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.basket_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.basket_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.wall_concrete
                or order.wall_hollow
                or order.wall_placo
                or order.wall_aluminum
                or order.wall_wood
                or order.wall_grumble_stone
                or order.wall_exterior_insulation
                or order.wall_other
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Mur")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Mur"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.wall_concrete:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Béton")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Béton", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.wall_hollow:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Creux")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Creux", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.wall_placo:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Placo")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Placo", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.wall_aluminum:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Aluminium")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Aluminium", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.wall_wood:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Bois")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Bois", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.wall_grumble_stone:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Rogne")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Rogne", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.wall_exterior_insulation:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Isolation extérieure")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Isolation extérieure", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.wall_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.wall_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.wall_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.protection_cardboard
                or order.protection_mr_store_carpet
                or order.protection_ribbon
                or order.protection_board
                or order.protection_barrier
                or order.protection_other
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Protection")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Protection"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.protection_cardboard:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Carton")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Carton", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.protection_mr_store_carpet:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Tapis MR Store")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Tapis MR Store", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.protection_ribbon:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Ruban")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Ruban", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.protection_board:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Planche")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Planche", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.protection_barrier:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Barrière")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Barrière", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.protection_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.protection_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.protection_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.forwarding_ropes
                or order.forwarding_lifting_kit
                or order.forwarding_shark_4
                or order.forwarding_shark_5
                or order.forwarding_shark_6
                or order.forwarding_other
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Acheminement")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Acheminement"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.forwarding_ropes:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Cordes")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Cordes", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.forwarding_lifting_kit:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit de levage")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit de levage", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.forwarding_shark_4:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Shark 4")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Shark 4", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.forwarding_shark_5:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Shark 5")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Shark 5", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.forwarding_shark_6:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Shark 6")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Shark 6", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.forwarding_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.forwarding_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.forwarding_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.silicon_transparent
                or order.silicon_white
                or order.silicon_ivory
                or order.silicon_black
                or order.silicon_brown
                or order.silicon_grey
                or order.silicon_anthracite
                or order.silicon_other
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Silicone")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Silicone"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.silicon_transparent:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Transparent")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Transparent", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.silicon_white:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Blanc")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Blanc", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.silicon_ivory:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Ivoire")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Ivoire", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.silicon_black:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Noir")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Noir", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.silicon_brown:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Marron")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Marron", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.silicon_grey:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Gris")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Gris", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.silicon_anthracite:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Anthracite")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Anthracite", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.silicon_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.silicon_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.silicon_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if order.glue_pergola_glue or order.glue_glue_gun or order.glue_other:
                installation_id = self.env["base.installation"].search([("name", "=", "Colle")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Colle"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.glue_pergola_glue:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Colle Pergola")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Colle Pergola", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.glue_glue_gun:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Pistolet à colle")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Pistolet à colle", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.glue_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.glue_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.glue_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if order.spray_aluminum_cleaner or order.spray_penetrating or order.spray_silicon_lubricant or order.spray_other:
                installation_id = self.env["base.installation"].search([("name", "=", "Bombe")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Bombe"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.spray_aluminum_cleaner:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Nettoyant Aluminium")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Nettoyant Aluminium", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.spray_penetrating:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Pénétrant")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Pénétrant", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.spray_silicon_lubricant:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Lubrifiant Silicone")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Lubrifiant Silicone", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.spray_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.spray_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.spray_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if order.paint_white or order.paint_ivory or order.paint_black or order.paint_grey or order.paint_brown or order.paint_anthracite or order.paint_other:
                installation_id = self.env["base.installation"].search([("name", "=", "Peinture")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Peinture"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.paint_white:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Blanc")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Blanc", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.paint_ivory:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Ivoire")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Ivoire", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.paint_black:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Noir")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Noir", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.paint_grey:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Gris")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Gris", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.paint_brown:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Marron")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Marron", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.paint_anthracite:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Anthracite")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Anthracite", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.paint_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.paint_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.paint_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.lifting_tool_1_elevator_3m
                or order.lifting_tool_2_elevator_3m
                or order.lifting_tool_1_elevator_38m
                or order.lifting_tool_2_elevator_38m
                or order.lifting_tool_1_manual_elevator_3m
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Outil de levage")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Outil de levage"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.lifting_tool_1_elevator_3m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "1 Monte charge 3M")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "1 Monte charge 3M", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.lifting_tool_2_elevator_3m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "2 Monte charge 3M")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "2 Monte charge 3M", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.lifting_tool_1_elevator_38m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "1 Monte charge 3,8M")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "1 Monte charge 3,8M", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.lifting_tool_2_elevator_38m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "2 Monte charge 3,8M")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "2 Monte charge 3,8M", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.lifting_tool_1_manual_elevator_3m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "1 Monte charge manuel 3M")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "1 Monte charge manuel 3M", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.tool_silicon_pump_18v
                or order.tool_suction_cup
                or order.tool_edger_220v
                or order.tool_long_drill_bit
                or order.tool_laser
                or order.tool_riveter
                or order.tool_big_angle_grinder_220v
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Outils")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Outils"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.tool_silicon_pump_18v:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Pompe à silicone 18V")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Pompe à silicone 18V", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.tool_suction_cup:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Ventouse")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Ventouse", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.tool_edger_220v:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Déligneuse 220V")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Déligneuse 220V", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.tool_long_drill_bit:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Longues Mèches")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Longues Mèches", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.tool_laser:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Laser")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Laser", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.tool_riveter:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Riveteuse")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Riveteuse", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.tool_big_angle_grinder_220v:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Grosse Disqueuse 220V")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Grosse Disqueuse 220V", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if order.saw_jigsaw or order.saw_milter_saw or order.saw_saber_220v or order.saw_saber_18v or order.saw_wood_circular:
                installation_id = self.env["base.installation"].search([("name", "=", "Scies")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Scies"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.saw_jigsaw:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Scie sauteuse")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Scie sauteuse", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.saw_milter_saw:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Scie à onglet")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Scie à onglet", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.saw_saber_220v:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Scie sabre 220V")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Scie sabre 220V", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.saw_saber_18v:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Scie sabre 18V")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Scie sabre 18V", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.saw_wood_circular:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Scie circulaire à bois")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Scie circulaire à bois", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if order.masonry_ruler_4m or order.masonry_ruler_5m or order.masonry_ruler_6m or order.masonry_other:
                installation_id = self.env["base.installation"].search([("name", "=", "Maçonnerie")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Maçonnerie"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.masonry_ruler_4m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Règle 4m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Règle 4m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.masonry_ruler_5m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Règle 5m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Règle 5m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.masonry_ruler_6m:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Règle 6m")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Règle 6m", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.masonry_other:
                    line_id = self.env["base.installation.line"].search([("name", "=", order.masonry_other)], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": order.masonry_other, "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]

            if (
                order.kit_iron_drill_bit
                or order.kit_pergola
                or order.kit_quiberon
                or order.kit_metal_curtain
                or order.kit_carpentry
                or order.kit_traditionnal_roller_shutter
                or order.kit_monobloc_roller_shutter
                or order.kit_bayblock_roller_shutter
                or order.kit_led
                or order.kit_manual_velum
                or order.kit_belt_velum
                or order.kit_cable_velum
                or order.kit_corded_grinder
                or order.kit_stapler
                or order.kit_rings
                or order.kit_hole_saw
            ):
                installation_id = self.env["base.installation"].search([("name", "=", "Kit")], limit=1)
                if not installation_id:
                    installation_id = self.env["base.installation"].create({"name": "Kit"})
                transaction_id = order.transaction_installation_ids.create({"base_installation_id": installation_id.id, "sale_order_id": order.id})
                if order.kit_iron_drill_bit:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit mèche fer")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit mèche fer", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_pergola:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit pergola")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit pergola", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_quiberon:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit quiberon")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit quiberon", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_metal_curtain:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit volet métallique")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit volet métallique", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_carpentry:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit charpente")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit charpente", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_traditionnal_roller_shutter:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit volet roulant traditionnel")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit volet roulant traditionnel", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_monobloc_roller_shutter:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit volet roulant monobloc")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit volet roulant monobloc", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_bayblock_roller_shutter:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit volet roulant bloc baie")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit volet roulant bloc baie", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_led:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit LED")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit LED", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_manual_velum:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit velum manuel")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit velum manuel", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_belt_velum:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit velum courroie")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit velum courroie", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_cable_velum:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit velum câble")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit velum câble", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_corded_grinder:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit meuleuse filaire")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit meuleuse filaire", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_stapler:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit agrafeuse")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit agrafeuse", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_rings:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit anneaux")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit anneaux", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
                if order.kit_hole_saw:
                    line_id = self.env["base.installation.line"].search([("name", "=", "Kit scie cloche")], limit=1)
                    if not line_id:
                        line_id = self.env["base.installation.line"].create({"name": "Kit scie cloche", "base_installation_id": installation_id.id})
                    transaction_id.base_installation_line_ids = [(4, line_id.id)]
