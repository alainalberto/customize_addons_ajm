from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class DiverDetails(models.Model):
    
    _name = 'driver.details'
    
    partner_id = fields.Many2one('res.partner', string='Customer')
    