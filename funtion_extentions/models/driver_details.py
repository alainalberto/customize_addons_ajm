from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class DiverDetails(models.Model):
    _name = 'driver.details'
    
    name = fields.Char(string="Name", related='resource_id.name', store=True, readonly=False, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    active = fields.Boolean('Active', related='resource_id.active', default=True, store=True, readonly=False)
    address_home_id = fields.Many2one(
        'res.partner', 'Address', help='Enter here the private address of the driver, not the one linked to your company.',
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    driving_license = fields.Binary(string="Driving License")
    phone = fields.Char(related='address_home_id.phone', related_sudo=False, readonly=False, string="Private Phone")
    notes = fields.Text('Notes')
    