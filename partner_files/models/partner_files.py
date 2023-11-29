# partner_files/models/models.py
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    file_ids = fields.One2many('partner.file', 'partner_id', string='Files')
    
    def action_create_file(self):
        self.ensure_one()
        return {
            'name': 'Add File',
            'type': 'ir.actions.act_window',
            'res_model': 'partner.file',
            'view_mode': 'form',
            'context': {'default_partner_id': self.id},
            'target': 'new',
        }
    
    def get_files_by_folder(self):
        folders = {}
        for file in self.file_ids:
            folder_name = file.folder_id.name if file.folder_id else 'Unclassified'
            if folder_name not in folders:
                folders[folder_name] = []
            folders[folder_name].append(file)
        return folders
    

class PartnerFile(models.Model):
    _name = 'partner.file'
    _description = 'Client Related File'

    name = fields.Char('File Name')
    file_data = fields.Binary('File', attachment=True, filename="name")
    folder_id = fields.Many2one('partner.folder', string='Folder')
    partner_id = fields.Many2one('res.partner', string='Customer')
    use_id = fields.Many2one('res.users', string='User')
    file_type = fields.Selection([('pdf', 'PDF'), ('doc', 'DOC'), ('xls', 'XLS'), ('jpg', 'JPG')], string='File Type')  
    
    

class PartnerFolder(models.Model):
    _name = 'partner.folder'
    _description = 'Client Related Folder'

    name = fields.Char('Folder Name')
    description = fields.Text('Description')
    folder_father = fields.Many2one('partner.folder', string='Folder Father')
   
    