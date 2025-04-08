# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TaskCardOrder(models.Model):
    _name = 'task.card.order'
    _description = '任务卡'

    name = fields.Char(string='任务卡名称', required=True)
    project_name = fields.Char(string='项目名称', required=True)
    project_manager = fields.Many2one('res.users', string='项目负责人')
    service_party_manager = fields.Many2one('res.users', string='服务方负责人')
    contract_number = fields.Char(string='合同编号')
    contract_name = fields.Char(string="合同名称")
    service_party_code = fields.Char(string='服务方编号')
    service_party_name = fields.Char(string='服务方名称')
    task_card_number = fields.Char(string='任务卡编号', required=True)
    department = fields.Char(string='任务提出部门')
    task_due_date = fields.Date(string='任务下发日期')
    task_description = fields.Text(string='任务说明')
    total_manday = fields.Float(string='任务周期 (天)')
    approver = fields.Many2one('res.users', string='审核人')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'portal_tsak_attachment_rel',
        'task_id', 'attachment_id',
        string='Attachments')
    task_list_ids = fields.One2many('task.card.order.line', 'task_card_id', string='任务清单')
    partner_id = fields.Many2one('res.partner', string='服务商名称')
    state = fields.Selection([
        ('draft', '草稿'),
        ('confirm', '已确认'),
        ('in', '进行中'),
        ('done', '已完成'),
        ('cancel', '已取消'),
    ], string='任务卡状态', default='draft')

    system_analyst = fields.Many2one("res.users", string="系统分析师")
    requirement_leader = fields.Many2one("res.users", string="需求提出部门领导")
    requirement_person = fields.Many2one("res.users", string="需求提出人")
    requirement_type = fields.Selection([
        ('functional', '功能性需求'),
        ('non_functional', '非功能性需求'),
        ('internal', '内部')
    ], string="提出类型")
    task_submission = fields.Date(string="任务提出时间")
    requirement_submission_time = fields.Date(string="需求提出时间")
    task_workload = fields.Float(string="工作量")
    task_items = fields.Text(string="任务项")
    task_card_download_date = fields.Date(string="任务卡下载日期")
    task_deadline = fields.Date(string="任务截止日期")
    development_progress = fields.Char(string="开发进度")
    progress_description = fields.Text(string="进度说明")
    is_overdue = fields.Boolean(string="是否超期")

    @api.model_create_multi
    def create(self, vals):
        """ 确保附件 public=True """
        res = super(TaskCardOrder, self).create(vals)
        if res.attachment_ids:
            res.attachment_ids.write({'public': True})
        return res

    def write(self, vals):
        """ 在附件更新时自动设置 public=True """
        res = super(TaskCardOrder, self).write(vals)
        if 'attachment_ids' in vals:
            self.attachment_ids.write({'public': True})
        return res


class TaskCardOrderLine(models.Model):
    _name = 'task.card.order.line'
    _description = '任务清单子表'

    task_card_id = fields.Many2one('task.card.order', string='任务卡', required=True, ondelete='cascade')
    task_item = fields.Char(string='任务项', required=True)
    project_manager = fields.Many2one('res.users', string='项目经理')
    developer = fields.Many2one('res.users', string='开发工程师')
    architect = fields.Many2one('res.users', string='架构工程师')
    product_manager = fields.Many2one('res.users', string='产品经理')
    ui_ux = fields.Many2one('res.users', string='UI/UE')
    tester = fields.Many2one('res.users', string='测试工程师')
    ops_engineer = fields.Many2one('res.users', string='运维工程师')
