# -*- coding: utf-8 -*-

from odoo import fields, models


class EisDragDropDemo(models.Model):
    _name = "mln_drag_drop.demo"
    _description = "mln Drag & Drop widget demo"

    name = fields.Char(string="Title", required=True, default="Widget demo")
    line_ids = fields.One2many(
        "mln_drag_drop.demo.line",
        "demo_id",
        string="Gallery (drag_drop_images)",
    )
