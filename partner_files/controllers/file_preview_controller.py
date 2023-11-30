from odoo import http
from odoo.http import request

class FilePreviewController(http.Controller):
    @http.route(['/files/preview/<int:file_id>'], type='http', auth="user")
    def preview_file(self, file_id, **kwargs):
        file_record = request.env['partner.file'].browse(file_id).sudo()
        if not file_record:
            return request.not_found()
        return http.Response(
            file_record.file_data,
            headers=[
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', 'attachment; filename="%s"' % file_record.name)
            ]
        )
