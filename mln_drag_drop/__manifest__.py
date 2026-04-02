# -*- coding: utf-8 -*-
{
    "name": "mln Drag Drop Gallery",
    "version": "18.0.1.5.9",
    "summary": "One2many image gallery: batch upload, lightbox preview, single & ZIP download (demo included)",
    "description": """
mln Drag Drop Gallery
=====================

Backend **one2many** image gallery — field widget **drag_drop_images**.

**Upload**
  * Drag multiple files onto the dashed area, or click *Drag or Upload* and select several images at once.
  * New child lines are created per file; the original file name is written to the child **name** field when present on the model.

**Preview**
  * Click a thumbnail to open a full-screen lightbox (Esc, backdrop click, or × to close).
  * Optional hover zoom via ``enable_zoom`` / ``enableZoom`` in options.

**Download**
  * Per-image download (no new browser tab; same-origin ``/web/image``).
  * *Download all (ZIP)* for saved child rows (save the parent form first so lines have database ids).

**Other**
  * Per-row remove (×); theme-friendly controls using ``span role="button"`` where needed.
  * Built-in **demo** menu: *mln Drag Drop → Demo* for reviewers and customers.

Docs: *README.md* and *static/description/index.html* (App Store listing).
    """,
    "category": "Web",
    "author": "melon",
    "license": "LGPL-3",
    "depends": ["web"],
    "data": [
        "security/ir.model.access.csv",
        "views/mln_drag_drop_demo_views.xml",
        "data/mln_drag_drop_demo_data.xml",
    ],
    "images": [
        "static/description/icon.png",
        "static/description/demo2.png",
    ],
    "assets": {
        "web.assets_backend": [
            "mln_drag_drop/static/src/js/drag_drop_images_field.js",
            "mln_drag_drop/static/src/xml/drag_drop_images_widgets.xml",
            "mln_drag_drop/static/src/scss/drag_drop_images_widgets.scss"
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 40,
    "currency": "EUR",
}
