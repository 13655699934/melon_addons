# -*- coding: utf-8 -*-

from odoo import fields, models


class EisDragDropDemoLine(models.Model):
    _name = "mln_drag_drop.demo.line"
    _description = "mln Drag & Drop demo line"
    _order = "sequence, id"

    demo_id = fields.Many2one(
        "mln_drag_drop.demo",
        string="Demo",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Label", default="Image")
    image_1920 = fields.Image(
        string="Image",
        max_width=1920,
        max_height=1920,
    )
