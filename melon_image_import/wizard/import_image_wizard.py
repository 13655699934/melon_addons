from odoo import _, api, fields, models
import base64
import zipfile
from io import BytesIO
from odoo import fields, models


class ImportImageWizard(models.TransientModel):
    _name = "package.import.image.wizard"
    _description = "Import Image wizard"

    def get_model_domain(self):
        field_ids = self.env["ir.model.fields"].search([("ttype", "=", "binary")])
        model_ids = (
            field_ids.mapped("model_id")
                .sorted("name")
                .filtered(lambda m: not m.model.startswith("ir.") and not m.transient)
        )
        return [("id", "in", model_ids.ids)]

    model_id = fields.Many2one("ir.model", string="Model", domain=get_model_domain)
    binary_field_id = fields.Many2one("ir.model.fields", string="Image Fields")
    package_file = fields.Binary(string="Zip Image")
    package_filename = fields.Char('Filename')
    match_name = fields.Selection([('name', 'name'), ('code', 'code'), ('auto', 'custom')], default='name',
                                  string='Match field',
                                  help=u'The image name in the zip package matches the unique value of the system')
    auto_define = fields.Char('logical name')

    def btn_confirm(self):
        """
           base64_data = base64.b64encode(f.read())
           zip包解析出数据目录格式说：img/0001.jpg
           常用方法：zf.split('/')[1]、a_f.startswith('S')
        """
        if self.package_filename:
            import_type = self.package_filename.split(".")[-1]
            if import_type != "zip":
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': u'File format error!',
                        'message': 'Please upload the zip file',
                        'sticky': False,
                        'className': 'bg-warning',
                        'type': 'warning',
                    },
                }
        zip_data = base64.decodebytes(self.package_file)
        model_name = self.model_id.model
        image_name = self.binary_field_id.name
        match_name = self.match_name
        if self.match_name == 'auto':
            match = self.auto_define
            match_name = match.strip(' ')
        fp = BytesIO()
        fp.write(zip_data)
        zip_f = zipfile.ZipFile(fp, "r")
        match_obj = self.env[model_name].sudo()
        no_find = []
        success_count = 0
        for zf in zip_f.namelist():
            aa = zip_f.open(zf, 'r')
            a_f = zf.split('/')[1]
            img_name = a_f.split('.')[0]
            if img_name:
                info_id = match_obj.search([(match_name, '=', img_name)], limit=1)
                if not info_id:
                    no_find.append(a_f)
                if info_id:
                    success_count += 1
                    info_id.write({image_name: base64.b64encode(aa.read())})
        zip_f.close()
        message = 'All pictures imported successfully'
        classname = 'bg-success'
        tip_type = 'success'
        if no_find:
            message = '【%s】pieces of data have been imported successfully，The following name picture [% s] ' \
                      'cannot find the corresponding record in the system' % (success_count, ','.join(no_find))
            classname = 'bg-warning'
            tip_type = 'warning'
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': u'Import results',
                'message': message,
                'sticky': True,
                'type': tip_type,
                'className': classname,
                'next': {
                    'type': 'ir.actions.act_window_close'
                },
            },
        }
        return notification


