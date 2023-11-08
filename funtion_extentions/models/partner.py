
from odoo import api, fields, models

class ResPartner(models.Model):
     _inherit = "res.partner"

     x_cliente_ssn = fields.Char(string="Social Security Number", tracking=True)
     x_cliente_ein = fields.Char(string="EIN", tracking=True)
     x_cliente_usdot = fields.Char(string="US_DOT", tracking=True, required=True)
     x_cliente_pin = fields.Char(string="US_DOT Pin", tracking=True )
     x_cliente_user = fields.Char(string="US_DOT User", tracking=True)
     x_cliente_pasw = fields.Char(string="US_DOT Password", tracking=True)
     x_cliente_mc = fields.Char(string="MC", tracking=True)
     x_cliente_tdmv = fields.Char(string="TDMV", tracking=True)
     x_cliente_login = fields.Char(string="Login", tracking=True)
     x_cliente_pass = fields.Char(string="Pass", tracking=True)
     x_cliente_uin = fields.Char(string="UIN", tracking=True)
     x_cliente_parking_address = fields.Char(string="Parking Lot Address", tracking=True)
     x_cliente_owner = fields.Char(string="Company Owner", tracking=True)
     customer_reference_id = fields.Many2one('res.partner', string='Customer Reference', domain="[('is_company', '=', False)]")
     driver_ids = fields.One2many('driver.details', 'partner_id', string='Drivers')
     vehicle_ids = fields.One2many('vehicle.details', 'partner_id', string='Vehicles')
     
     def action_create_driver(self):
        self.ensure_one()
        return {
            'name': 'Create Driver',
            'type': 'ir.actions.act_window',
            'res_model': 'driver.details',
            'view_mode': 'form',
            'context': {'default_partner_id': self.id},
            'target': 'new',
        }
        
     def action_create_vehicle(self):
        self.ensure_one()
        return {
            'name': 'Create Vehicle',
            'type': 'ir.actions.act_window',
            'res_model': 'vehicle.details',
            'view_mode': 'form',
            'context': {'default_partner_id': self.id},
            'target': 'new',
        }





     
