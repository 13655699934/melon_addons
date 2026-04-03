# -*- coding: utf-8 -*-
{
    "name": "mln Advanced List View",
    "version": "18.0.1.0.0",
    "summary": "List views: per-column filters, row numbers, PDF/Excel/CSV export, copy — any main window model",
    "description": """
mln Advanced List View (Odoo 18)
================================

Enhance standard backend list views with productivity tools that work on **any model**
opened as a main window list (search panel + list).

**Highlights**
--------------

* **Per-column quick filters** — one text field per visible column (where the field type allows it): char, text, html, numeric, monetary, boolean, selection, many2one, **date/datetime** (e.g. year, month, or full day), **many2many** (name search on related records). Filters combine with the global search/domain.
* **Row numbers (N°)** — index column aligned with the list, pager-aware.
* **Export** — **PDF**, **Excel** (.xlsx), **CSV** (UTF-8 with BOM). File names use the model’s **display name** from *ir.model* (or *_description*).
* **Copy** — copy the current grid as tab-separated values.
* **Toolbar** — export menu, copy, reset column filters.
* **Per-user preferences** (server-side) — optional inline-edit behaviour and stored filter metadata via *mln.advanced.list.preference* (for integrators / future UI).

**Dependencies**
----------------

* **web** — required.
* **account** — required so list views that use the *file_upload_list* renderer (e.g. some Sales flows) get the same toolbar and filters.

**Technical**
-------------

* Client: OWL patches on list controller, renderer, and relational model load.
* Server: export RPC; PDF uses ReportLab (CJK-friendly fonts if available on the server or under *static/fonts/*); Excel uses *xlsxwriter*.

**License:** LGPL-3
""",
    "category": "Web",
    "author": "melon",
    "license": "LGPL-3",
    "depends": ["web"],
    "data": [
        "security/ir.model.access.csv",
        "security/mln_advanced_list_security.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mln_advanced_list/static/src/scss/mln_advanced_list.scss",
            "mln_advanced_list/static/src/xml/mln_list_templates.xml",
            "mln_advanced_list/static/src/xml/mln_list_templates_file_upload.xml",
            "mln_advanced_list/static/src/js/mln_advanced_list_service.js",
            "mln_advanced_list/static/src/js/relational_model_patch.js",
            "mln_advanced_list/static/src/js/list_controller_patch.js",
            "mln_advanced_list/static/src/js/list_renderer_patch.js",
            "mln_advanced_list/static/src/js/mln_advanced_list.js",
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 40,
    "currency": "EUR",
}
