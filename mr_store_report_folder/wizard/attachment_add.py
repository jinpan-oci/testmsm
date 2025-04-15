from odoo import fields, models


class AttachmentAdd(models.TransientModel):
    _name = "attachment.add"
    _description = "Add Attachment into saleorder"
    file_name = fields.Char("File Name", required=True)
    file = fields.Binary("File", required=True)
    usetype = fields.Selection(
        [
            ("before_installation", "Photo Before Installation"),
            ("with_3d", "Photo With 3D"),
            ("mesures", "Mesures Drawings"),
        ],
        string="Photo Use Type",
        default="before_installation",
    )

    def action_add_attachment(self):
        self.env["ir.attachment"].create(
            {
                "name": self.file_name,
                "datas": self.file,
                "res_model": "sale.order",
                "res_id": self.env.context["active_id"],
                "photo_use_type": self.usetype,
            }
        )
        return {"type": "ir.actions.act_window_close"}
