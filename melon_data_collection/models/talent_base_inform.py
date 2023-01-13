from odoo import api, fields, models


class TalentBaseInform(models.Model):
    _name = 'talent.base.inform'
    _inherit = ['mail.thread']
    _description = "人员信息表"
    _check_company_auto = True
    _rec_name = 'name'
    _order = 'write_date ASC, create_date ASC'

    name = fields.Char(string='姓名', index=True, tracking=True)
    age = fields.Integer(u'年龄')
    ID_number = fields.Char(string='证件号码', tracking=True)
    graduation_school = fields.Char(string='毕业院校', tracking=True)
    major_studied = fields.Char(string='所学专业', tracking=True)
    company_id = fields.Many2one('res.company', string='工作单位', index=True, tracking=True,
                                 default=lambda self: self.env.company)
    project_info_ids = fields.One2many('project.base.detail', inverse_name='inform_id', string='项目信息',
                                       ondelete='cascade')
    by_import = fields.Boolean(u'是导入数据')

    @api.model
    def create(self, vals):
        res = super(TalentBaseInform, self).create(vals)
        return res

    def btn_info_import(self):
        return {
            'name': '信息导入',
            'view_mode': 'form',
            'res_model': 'import.talent.info.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'res_id': self.id}
        }


class ProjectBaseDetail(models.Model):
    _name = 'project.base.detail'
    _description = '项目信息'
    _order = 'create_date desc'

    code = fields.Char(string='项目编号', tracking=True)
    name = fields.Char(string="项目名称", tracking=True)
    description = fields.Char(string='项目描述', tracking=True)
    inform_id = fields.Many2one('talent.base.inform', string="人员信息", ondelete='cascade')
