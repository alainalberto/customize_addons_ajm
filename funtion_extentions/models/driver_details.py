from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class DiverDetails(models.Model):
    _name = 'driver.details'
    
    name = fields.Char(string="Name", store=True, readonly=False, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    active = fields.Boolean(string ='Active', default=True, store=True, readonly=False)
    address_home_id = fields.Text(string="Home Address")
    driving_license = fields.Binary(string="Driving License")
    phone = fields.Char( related_sudo=False, readonly=False, string="Private Phone")
    notes = fields.Text('Notes')
    