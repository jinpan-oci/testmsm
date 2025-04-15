import base64
from io import BytesIO

from odoo import SUPERUSER_ID, http
from odoo.http import request
from odoo.tools.misc import file_open
from PIL import Image


class ImageProvider(http.Controller):
    # create a /get_image/model_name/id/field_name route that returns the image
    @http.route(
        "/get_image/<string:model_name>/<int:id>/<string:field_name>",
        type="http",
        auth="none",
    )
    def get_image(self, model_name, id, field_name, **kwargs):
        record = request.env[model_name].with_user(SUPERUSER_ID).sudo().browse(id)
        image_field = record[field_name]
        default_image = file_open(
            "base_sync_master/static/description/placeholder.png", "rb"
        ).read()
        if image_field and type(image_field) is bytes:
            image = base64.b64decode(image_field)
            if image and type(image) is bytes:
                image_pil = Image.open(BytesIO(image))
                try:
                    image_pil.verify()
                    if image_pil.format == "PNG":
                        return request.make_response(
                            data=image,
                            headers=[("Content-Type", "image/png")],
                        )
                    elif image_pil.format == "JPEG":
                        return request.make_response(
                            data=image,
                            headers=[("Content-Type", "image/jpeg")],
                        )
                    elif image_pil.format == "JPG":
                        return request.make_response(
                            data=image,
                            headers=[("Content-Type", "image/jpg")],
                        )
                    else:
                        return request.make_response(
                            data=image,
                            headers=[("Content-Type", "image/png")],
                        )
                except Exception:
                    pass
        return request.make_response(
            data=default_image,
            headers=[("Content-Type", "image/png")],
        )
