# Part of Connector ANKORSTORE. See LICENSE file for full copyright and licensing details.
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class SyncWebhookController(http.Controller):
    @http.route(
        "/sync/webhooks/base_sync",
        type="json",
        methods=["POST"],
        auth="none",
        csrf=False,
    )
    def webhook_(self, **post):
        # main controller for handling webhooks
        # import pdb; pdb.set_trace()
        posted_data = request.httprequest.get_data()
        data = json.loads(posted_data)
        base_sync_id = data.get("base_sync_id")
        try:
            request.env["base.sync"].with_context(
                lang="en_US"
            ).sudo().generate_line_ids(base_sync_id)
            return {"status": "200"}
        except Exception as e:
            _logger.exception("Error processing AKS webhook: %s", e)
            return {"status": "error", "message": str(e)}
