# partner_files/models/models.py
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    file_ids = fields.One2many('partner.file', 'partner_id', string='Files')
    folder_ids = fields.One2many('partner.folder', 'partner_id', string='Folders')


class PartnerFile(models.Model):
    _name = 'partner.file'
    _description = 'Client Related File'

    name = fields.Char('File Name')
    file_data = fields.Binary('File', attachment=True)
    folder_id = fields.Many2one('partner.folder', string='Folder')
    partner_id = fields.Many2one('res.partner', string='Customer')

class PartnerFolder(models.Model):
    _name = 'partner.folder'
    _description = 'Client Related Folder'

    name = fields.Char('Folder Name')
    partner_id = fields.Many2one('res.partner', string='Customer')
    file_ids = fields.One2many('partner.file', 'folder_id', string='Files')