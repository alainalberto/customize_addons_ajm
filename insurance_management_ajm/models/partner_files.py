
from odoo import models, fields, api

class PartnerFiles(models.Model):
    _inherit = 'partner_file'

    policy_id = fields.Many2one('policy.details', string='Policy', delete='cascade')

    @api.model
    def create(self, vals):
        # Create parent folder if it doesn't exist
        partner_id = vals.get('partner_id')
        parent_folder = self.env['ir.attachment.folder'].search([('partner_id', '=', partner_id)])
        if not parent_folder:
            parent_folder = self.env['ir.attachment.folder'].create({
                'name': 'Parent Folder',
                'partner_id': partner_id,
            })

        # Create child folder if it doesn't exist
        insurance_folder = self.env['ir.attachment.folder'].search([('name', '=', 'INSURANCE'), ('parent_id', '=', parent_folder.id)])
        if not insurance_folder:
            insurance_folder = self.env['ir.attachment.folder'].create({
                'name': 'INSURANCE',
                'parent_id': parent_folder.id,
            })

        # Save the files
        files = vals.get('files')
        if files:
            for file in files:
                self.env['ir.attachment'].create({
                    'name': file.get('name'),
                    'datas': file.get('datas'),
                    'res_model': self._name,
                    'res_id': self.id,
                    'folder_id': insurance_folder.id,
                })

        return super(PartnerFiles, self).create(vals)
    