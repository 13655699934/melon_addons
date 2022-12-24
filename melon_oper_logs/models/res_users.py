# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import api, fields, models


def is_boolean_group(name):
    """
    Boolean类型权限组
    """
    return name.startswith('in_group_')


def is_selection_groups(name):
    """
        selection类型权限组
    """
    return name.startswith('sel_groups_')


def is_reified_group(name):
    """
    区别权限组属于什么类型
    """
    return is_boolean_group(name) or is_selection_groups(name)
