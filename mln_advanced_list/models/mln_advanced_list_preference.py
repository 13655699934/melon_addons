# -*- coding: utf-8 -*-
import base64
import csv
import io
import logging
import os
import re

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from odoo.modules import module as odoo_module
from odoo.tools.misc import xlsxwriter

_logger = logging.getLogger(__name__)

# Cache (regular_name, bold_name) for reportlab after first successful registration
_mln_pdf_font_cache = None


def _mln_try_register_ttfont(pdfmetrics, ttfont_cls, path, font_name, subfont_index=0):
    if not path or not os.path.isfile(path):
        return False
    try:
        pdfmetrics.registerFont(ttfont_cls(font_name, path, subfontIndex=subfont_index))
        return True
    except Exception as err:  # noqa: BLE001
        _logger.debug("mln_advanced_list: skip font %s: %s", path, err)
        return False


def _mln_pdf_unicode_font_pair():
    """Return (regular_font_name, bold_font_name) registered in reportlab for CJK/Unicode PDF."""
    global _mln_pdf_font_cache
    if _mln_pdf_font_cache is not None:
        return _mln_pdf_font_cache
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        _mln_pdf_font_cache = ("Helvetica", "Helvetica-Bold")
        return _mln_pdf_font_cache

    reg = "MlnAdvListPdf"
    bold = "MlnAdvListPdfBd"
    regular_paths = []
    mod_path = odoo_module.get_module_path("mln_advanced_list")
    if mod_path:
        bundled = os.path.join(mod_path, "static", "fonts")
        if os.path.isdir(bundled):
            for fn in sorted(os.listdir(bundled)):
                low = fn.lower()
                if low.endswith((".ttf", ".otf", ".ttc")):
                    regular_paths.append(os.path.join(bundled, fn))
    regular_paths.extend(
        [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-VF.ttf",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/arphic/uming.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "msyh.ttc"),
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "msyh.ttf"),
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "simhei.ttf"),
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "simsun.ttc"),
        ]
    )
    bold_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "msyhbd.ttc"),
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "simhei.ttf"),
    ]

    for subidx in (0, 1):
        for path in regular_paths:
            if _mln_try_register_ttfont(pdfmetrics, TTFont, path, reg, subfont_index=subidx):
                bold_ok = False
                for bp in bold_paths:
                    if _mln_try_register_ttfont(pdfmetrics, TTFont, bp, bold, subfont_index=subidx):
                        bold_ok = True
                        break
                if not bold_ok:
                    try:
                        pdfmetrics.registerFont(
                            TTFont(bold, path, subfontIndex=subidx)
                        )
                    except Exception:  # noqa: BLE001
                        bold = reg
                _mln_pdf_font_cache = (reg, bold)
                return _mln_pdf_font_cache

    _logger.warning(
        "mln_advanced_list: no Unicode/CJK font found for PDF export. "
        "Install fonts-noto-cjk (Linux), use macOS built-in fonts, or place a "
        ".ttf/.otf/.ttc in mln_advanced_list/static/fonts/"
    )
    _mln_pdf_font_cache = ("Helvetica", "Helvetica-Bold")
    return _mln_pdf_font_cache


def _mln_pdf_content_has_non_latin(table_data):
    for row in table_data:
        for cell in row:
            if cell is None or cell is False:
                continue
            s = str(cell)
            for ch in s:
                if ord(ch) > 0xFF:
                    return True
    return False


def _mln_export_label_for_model(env, res_model):
    """Human label: ir.model name (translated), else model _description, else technical name."""
    if not res_model or not isinstance(res_model, str):
        return _("Export")
    if res_model not in env:
        return res_model.replace(".", "_")
    try:
        im = env["ir.model"].sudo()._get(res_model)
        if im.exists() and (im.name or "").strip():
            return (im.name or "").strip()
    except Exception:  # noqa: BLE001
        pass
    try:
        Model = env[res_model]
        desc = getattr(Model, "_description", None)
        if desc and str(desc).strip():
            return str(desc).strip()
    except KeyError:
        pass
    return res_model.replace(".", "_")


def _mln_safe_filename_stem(label, max_len=120):
    """ASCII-safe stem for downloaded files; keeps Unicode letters for CJK etc."""
    if not label:
        return "export"
    s = str(label).strip()
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", s)
    s = re.sub(r"\s+", " ", s).strip(" .")
    if not s:
        return "export"
    if len(s) > max_len:
        s = s[:max_len].rstrip(" .")
    return s or "export"


def _mln_xlsx_worksheet_name(label):
    """Excel worksheet name max 31 chars, no : \\ / ? * [ ]"""
    s = _mln_safe_filename_stem(label, max_len=31)
    s = re.sub(r"[:\\/?*\[\]]", "_", s)[:31]
    return s or "Sheet1"


class MlnAdvancedListFilterLine(models.Model):
    _name = "mln.advanced.list.filter.line"
    _description = "Advanced list column filter definition"
    _order = "sequence, id"

    preference_id = fields.Many2one(
        "mln.advanced.list.preference", required=True, ondelete="cascade"
    )
    sequence = fields.Integer(default=10)
    field_name = fields.Char(required=True)
    label = fields.Char()
    placeholder = fields.Char()


class MlnAdvancedListPreference(models.Model):
    _name = "mln.advanced.list.preference"
    _description = "Per-user advanced list view options"
    _rec_name = "res_model"

    user_id = fields.Many2one(
        "res.users", required=True, default=lambda self: self.env.user, index=True
    )
    res_model = fields.Char(string="Model technical name", required=True, index=True)
    inline_edit = fields.Boolean(default=True)
    filter_line_ids = fields.One2many(
        "mln.advanced.list.filter.line", "preference_id", string="Column filters"
    )

    _sql_constraints = [
        (
            "mln_adv_list_pref_user_model_uniq",
            "unique(user_id, res_model)",
            "Only one advanced list preference per user and model.",
        ),
    ]

    @api.model
    def mln_get_for_user_model(self, res_model):
        if not self.env.user or self.env.user._is_public():
            raise AccessError(_("You must be logged in."))
        pref = self.search(
            [("user_id", "=", self.env.user.id), ("res_model", "=", res_model)], limit=1
        )
        if not pref:
            return {
                "id": False,
                "res_model": res_model,
                "inline_edit": True,
                "filter_lines": [],
            }
        lines = []
        for line in pref.filter_line_ids.sorted("sequence"):
            lines.append(
                {
                    "field_name": line.field_name,
                    "label": line.label or line.field_name,
                    "placeholder": line.placeholder or "",
                }
            )
        return {
            "id": pref.id,
            "res_model": pref.res_model,
            "inline_edit": pref.inline_edit,
            "filter_lines": lines,
        }

    def _mln_ensure_own(self):
        for rec in self:
            if rec.user_id != self.env.user:
                raise AccessError(_("You can only access your own list preferences."))

    def mln_save_preference(self, vals):
        """vals: { inline_edit: bool, filter_lines: [{field_name, label, placeholder}, ...] }"""
        self.ensure_one()
        self._mln_ensure_own()
        self.inline_edit = bool(vals.get("inline_edit", True))
        self.filter_line_ids.unlink()
        lines = vals.get("filter_lines") or []
        for i, line in enumerate(lines):
            self.env["mln.advanced.list.filter.line"].create(
                {
                    "preference_id": self.id,
                    "sequence": 10 * (i + 1),
                    "field_name": line.get("field_name"),
                    "label": line.get("label") or line.get("field_name"),
                    "placeholder": line.get("placeholder") or "",
                }
            )
        return self.mln_get_for_user_model(self.res_model)

    @api.model
    def mln_create_or_update(self, res_model, vals):
        if not self.env.user or self.env.user._is_public():
            raise AccessError(_("You must be logged in."))
        pref = self.search(
            [("user_id", "=", self.env.user.id), ("res_model", "=", res_model)], limit=1
        )
        if not pref:
            lines_spec = vals.get("filter_lines")
            if lines_spec is None:
                o2m = []
            else:
                o2m = [
                    (
                        0,
                        0,
                        {
                            "sequence": 10 * (i + 1),
                            "field_name": line.get("field_name"),
                            "label": line.get("label") or line.get("field_name"),
                            "placeholder": line.get("placeholder") or "",
                        },
                    )
                    for i, line in enumerate(lines_spec)
                ]
            pref = self.create(
                {
                    "user_id": self.env.user.id,
                    "res_model": res_model,
                    "inline_edit": bool(vals.get("inline_edit", True)),
                    "filter_line_ids": o2m,
                }
            )
        else:
            pref.mln_save_preference(vals)
        return pref.mln_get_for_user_model(res_model)

    @api.model
    def mln_export_file(self, export_format, headers, rows, res_model=None):
        """export_format: 'csv' | 'xlsx' | 'pdf' — returns {filename, mimetype, data_b64}.

        File base name uses ir.model name (UI / translated) or model _description.
        """
        if not self.env.user or self.env.user._is_public():
            raise AccessError(_("You must be logged in."))
        headers = headers or []
        rows = rows or []
        label = _mln_export_label_for_model(self.env, res_model)
        stem = _mln_safe_filename_stem(label)
        if export_format == "csv":
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
            data = buf.getvalue().encode("utf-8-sig")
            return {
                "filename": f"{stem}.csv",
                "mimetype": "text/csv;charset=utf-8",
                "data_b64": base64.b64encode(data).decode(),
            }
        if export_format == "xlsx":
            if not xlsxwriter:
                raise UserError(_("Excel export requires the xlsxwriter library."))
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {"in_memory": True})
            sheet = workbook.add_worksheet(_mln_xlsx_worksheet_name(label))
            for c, h in enumerate(headers):
                sheet.write(0, c, h)
            for r, row in enumerate(rows, start=1):
                for c, cell in enumerate(row):
                    sheet.write(r, c, cell)
            workbook.close()
            data = output.getvalue()
            return {
                "filename": f"{stem}.xlsx",
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "data_b64": base64.b64encode(data).decode(),
            }
        if export_format == "pdf":
            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import landscape, A4
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
            except ImportError as e:
                raise UserError(_("PDF export requires reportlab: %s") % e) from e
            output = io.BytesIO()
            doc = SimpleDocTemplate(
                output,
                pagesize=landscape(A4),
                leftMargin=18,
                rightMargin=18,
                topMargin=18,
                bottomMargin=18,
            )
            def _cell(v):
                return "" if v is None or v is False else str(v)

            table_data = [[_cell(c) for c in headers]] + [
                [_cell(c) for c in row] for row in rows
            ] if headers else [[_cell(c) for c in row] for row in rows]
            if not table_data:
                table_data = [[""]]
            col_count = max(len(r) for r in table_data)
            normalized = [list(r) + [""] * (col_count - len(r)) for r in table_data]
            font_reg, font_bold = _mln_pdf_unicode_font_pair()
            if _mln_pdf_content_has_non_latin(normalized) and font_reg == "Helvetica":
                raise UserError(
                    _(
                        "PDF export needs a font that supports your language (e.g. Chinese). "
                        "On Linux install package fonts-noto-cjk, or copy a .ttf/.ttc font file into "
                        "folder static/fonts/ inside the mln_advanced_list module, then restart Odoo."
                    )
                )
            table = Table(normalized, repeatRows=1 if headers else 0)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5E4B9A")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("FONTNAME", (0, 0), (-1, 0), font_bold),
                        ("FONTNAME", (0, 1), (-1, -1), font_reg),
                        ("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F3FF")]),
                    ]
                )
            )
            doc.build([table])
            data = output.getvalue()
            return {
                "filename": f"{stem}.pdf",
                "mimetype": "application/pdf",
                "data_b64": base64.b64encode(data).decode(),
            }
        raise UserError(_("Unknown export format."))
