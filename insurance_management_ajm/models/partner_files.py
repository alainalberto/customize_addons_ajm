
from odoo import models, fields, api

class PartnerFiles(models.Model):
    _inherit = 'partner.file'

    policy_id = fields.Many2one('policy.details', string='Policy', delete='cascade')

    @api.model
    def create(self, vals):
        policy_id = self.env['policy.details'].browse(vals['policy_id']) 

        # Buscar o crear el policy folder
        folder_name = policy_id.tag_display  
        folder = self.env['partner.folder'].search([('name', '=', folder_name)], limit=1)
        if not folder:
            folder_vals = {
                'name': folder_name,
                'description': folder_name,
            }
            folder = self.env['partner.folder'].create(folder_vals)

        # Asignar el folder_id y crear el archivo
        vals['folder_id'] = folder.id
        vals['policy_id'] = policy_id.id
        vals['use_id'] = self.env.uid
        vals['partner_id'] = policy_id.partner_id.id
        return super(PartnerFiles, self).create(vals)