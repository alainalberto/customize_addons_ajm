from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class TypeVehicle(models.Model):
    _name = 'vehicle.type'
    
    name = fields.Char(string="Name of Type", required=True)
    description = fields.Text(string="Description of Type", required=True)


class VehicleDetails(models.Model):
    _name = 'vehicle.details'
    
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    driver_id = fields.Many2one('driver.details', string='Driver')
    type_id = fields.Many2one('vehicle.type', string='Type')
    vin_number = fields.Char(string="VIN Number")
    make = fields.Char(string="Make")
    year = fields.Integer(string="Year")
    model = fields.Char(string="Model")
    license_plate = fields.Char(string="License Plate")
    description = fields.Text(string="Description")
    registration_exp_date = fields.Date(string='Registration Expiration Date')
    use = fields.Selection(
        [('personal', 'Personal'), ('commercial', 'Commercial'), ('both', 'Both')], default='commercial', string='Use Type')  