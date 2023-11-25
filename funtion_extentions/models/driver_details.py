from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class DiverDetails(models.Model):
    _name = 'driver.details'
    
    name = fields.Char(string="Name", store=True, readonly=False, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    active = fields.Boolean(string ='Active', default=True, store=True, readonly=False)
    address_home_id = fields.Text(string="Home Address")
    phone = fields.Char( related_sudo=False, readonly=False, string="Private Phone")
    driver_lic_number_1 = fields.Char(string="Driver License Number")
    driver_lic_state_1 = fields.Char(string="Driver License State")
    driver_lic_expiration_1 = fields.Date(string="Driver License Expiration")
    driver_lic_front_1 = fields.Binary(string="Driving License Front")
    driver_lic_back_1 = fields.Binary(string="Driving License Back")
    driver_lic_number_2 = fields.Char(string="Driver License Number")
    driver_lic_state_2 = fields.Char(string="Driver License State")
    driver_lic_expiration_2 = fields.Date(string="Driver License Expiration")
    driver_lic_front_2 = fields.Binary(string="Driving License Front")
    driver_lic_back_2 = fields.Binary(string="Driving License Back")
    medical_card_number = fields.Char(string="Medical Card Number")
    medical_card_expiration = fields.Date(string="Medical Card Expiration")
    medical_card_file = fields.Binary(string="Medical Card")
    notes = fields.Text('Notes')
    