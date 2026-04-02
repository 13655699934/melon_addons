# -*- coding: utf-8 -*-

import base64
import io
import json
import os
import zipfile

from odoo import http, _
from odoo.exceptions import AccessError, UserError
from odoo.http import content_disposition, request


_VALID_IMG_EXT = frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"})


def _zip_entry_name(record, used_names, index):
    if "name" in record._fields:
        raw_name = (record.name or "").strip()
    else:
        raw_name = ""
    base = raw_name or _("image_%s") % record.id
    root, ext = os.path.splitext(base)
    if ext.lower() in _VALID_IMG_EXT:
        stem = root or "image"
        use_ext = ext
    else:
        stem = base if base else "image"
        use_ext = ".png"
    safe_stem = "".join(c if c.isalnum() or c in " ._-" else "_" for c in stem)[:120].strip() or "image"
    candidate = f"{safe_stem}{use_ext}"
    if candidate not in used_names:
        used_names.add(candidate)
        return candidate
    candidate = f"{safe_stem}_{record.id}{use_ext}"
    if candidate not in used_names:
        used_names.add(candidate)
        return candidate
    candidate = f"{safe_stem}_{record.id}_{index}{use_ext}"
    used_names.add(candidate)
    return candidate


class MlnDragDropGalleryZipController(http.Controller):
    @http.route(
        "/mln_drag_drop/gallery_images_zip",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=True,
    )
    def gallery_images_zip(self, **kwargs):
        """Build a zip of binary/image fields for given record ids (same model)."""
        model = kwargs.get("model") or request.httprequest.form.get("model")
        field = kwargs.get("field") or request.httprequest.form.get("field")
        line_ids_raw = kwargs.get("line_ids") or request.httprequest.form.get("line_ids") or "[]"

        if not model or not field:
            return request.make_response(
                json.dumps({"error": "missing model or field"}),
                headers=[("Content-Type", "application/json")],
                status=400,
            )

        try:
            ids = json.loads(line_ids_raw)
        except (json.JSONDecodeError, TypeError):
            return request.make_response(
                json.dumps({"error": "invalid line_ids"}),
                headers=[("Content-Type", "application/json")],
                status=400,
            )

        if not isinstance(ids, list) or not ids:
            return request.make_response(
                json.dumps({"error": "no ids"}),
                headers=[("Content-Type", "application/json")],
                status=400,
            )

        try:
            Model = request.env[model]
        except KeyError:
            return request.make_response(
                json.dumps({"error": "unknown model"}),
                headers=[("Content-Type", "application/json")],
                status=400,
            )

        field_obj = Model._fields.get(field)
        if not field_obj or field_obj.type not in ("binary", "image"):
            return request.make_response(
                json.dumps({"error": "invalid field"}),
                headers=[("Content-Type", "application/json")],
                status=400,
            )

        try:
            records = Model.browse([int(i) for i in ids])
            records.check_access("read")
            records.read([field, "name"] if "name" in Model._fields else [field])
        except (AccessError, UserError, ValueError, TypeError):
            return request.make_response(
                json.dumps({"error": "access denied"}),
                headers=[("Content-Type", "application/json")],
                status=403,
            )

        buf = io.BytesIO()
        used_names = set()
        index = 0
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for rec in records:
                data = rec[field]
                if not data:
                    continue
                index += 1
                if isinstance(data, memoryview):
                    raw = data.tobytes()
                elif isinstance(data, bytes):
                    raw = data
                else:
                    try:
                        raw = base64.b64decode(data)
                    except (TypeError, ValueError):
                        continue
                if not raw:
                    continue
                entry = _zip_entry_name(rec, used_names, index)
                zf.writestr(entry, raw)

        payload = buf.getvalue()
        if not payload:
            return request.make_response(
                json.dumps({"error": "no image data"}),
                headers=[("Content-Type", "application/json")],
                status=400,
            )

        headers = [
            ("Content-Type", "application/zip"),
            ("Content-Length", len(payload)),
            ("Content-Disposition", content_disposition("gallery_images.zip")),
        ]
        return request.make_response(payload, headers=headers)
