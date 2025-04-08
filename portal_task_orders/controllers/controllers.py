from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
from odoo.osv.expression import OR

class CustomerPortal(portal.CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        task_count = request.env['task.card.order'].sudo().search_count([('partner_id', '=', partner.id)])
        values.update({
            'task_count': task_count,
        })
        return values

    @http.route(['/my/card/task/orders', '/my/card/task/orders/page/<int:page>'], type='http', auth="user",cors="*",)
    def portal_my_orders(self, page=1, search=None, search_in='all', **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        if search:
            domain = OR([domain, [('name', 'ilike', search)], [('task_card_number', 'ilike', search)]])
        task_count = request.env['task.card.order'].sudo().search_count(domain)
        pager = portal_pager(url="/my/card/task/orders", total=task_count, page=page, step=10)
        tasks = request.env['task.card.order'].sudo().search(domain, order="create_date desc", limit=10, offset=pager['offset'])
        values.update({
            'task_cards': tasks,
            'pager': pager,
            'search': search,
            'languages': [],  # 确保语言数据存在
        })
        return request.render("portal_task_orders.portal_task_temp_001", values)

    @http.route('/my/card/task/order/<int:task_id>', type='http', auth="user",cors="*",)
    def portal_task_order_detail(self, task_id, **kw):
        partner = request.env.user.partner_id
        task = request.env['task.card.order'].sudo().browse(task_id)
        print('==task===',task)
        print('==task_id===',task_id)

        if not task.exists() or task.partner_id.id != partner.id:
            return request.redirect('/my/card/task/orders')
        values = {
            'task': task,
            'languages': [],  # 确保语言数据存在
        }
        return request.render("portal_task_orders.portal_task_detail_001", values)

    @http.route('/my/card/task/orders/edit/<int:task_id>', type='http', auth='user',cors="*")
    def edit_task(self, task_id, **kwargs):
        task = request.env['task.card.order'].sudo().browse(task_id)
        if not task.exists():
            return request.redirect('/my/card/task/orders')
        return request.render("portal_task_orders.portal_task_edit_001", {"task": task,'languages': []})

    @http.route('/my/card/task/orders/update', type='http', auth='user', methods=['POST'],cors="*")
    def update_task(self, **kwargs):
        task_id = int(kwargs.get("task_id"))
        task = request.env['task.card.order'].sudo().browse(task_id)
        if task.exists():
            task.sudo().write({
                "name": kwargs.get("name"),
                "task_card_number": kwargs.get("task_card_number"),
                "project_name": kwargs.get("project_name"),
                "contract_number": kwargs.get("contract_number"),
                "task_description": kwargs.get("task_description"),
            })
        return request.redirect('/my/card/task/orders')


    @http.route('/my/task/orders', type='http', auth="user",cors="*")
    def portal_my_tasks(self, **kwargs):
        values = self._prepare_portal_layout_values()
        domain = []
        project_name = kwargs.get('project_name')
        contract_number = kwargs.get('contract_number')
        state = kwargs.get('state')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        if project_name:
            domain.append(('project_name', 'ilike', project_name))
        if contract_number:
            domain.append(('contract_number', 'ilike', contract_number))
        if state:
            domain.append(('state', '=', state))
        if start_date and end_date:
            domain.append(('task_due_date', '>=', start_date))
            domain.append(('task_due_date', '<=', end_date))

        task_count = request.env['task.card.order'].sudo().search_count(domain)
        pager = portal_pager(url="/my/card/task/orders", total=task_count, page=1, step=10)
        tasks = request.env['task.card.order'].sudo().search(domain, order="create_date desc", limit=10, offset=pager['offset'])
        values.update({
            'task_cards': tasks,
            'pager': pager,
            'languages': [],  # 确保语言数据存在
        })
        return request.render("portal_task_orders.portal_task_temp_001", values)

