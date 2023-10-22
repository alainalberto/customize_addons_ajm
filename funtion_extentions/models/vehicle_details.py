from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class TypeVehicle(models.Model):
    _name = 'vehicle.type'
    
    name = fields.char(string="Name of Type", required=True)
    description = fields.char(string="Drescription of Type", required=True)
    

    class Meta:
        verbose_name = _("TypeVehicle")
        verbose_name_plural = _("TypeVehicles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("TypeVehicle_detail", kwargs={"pk": self.pk})




class VehicleDetails(models.Model):
    _name = 'vehicle.details'
    
    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    diverr_id = fields.Many2one('driver.details', string='Driver')
    type_id = fields.Many2one('vehicle.type', string='Type')
    vin_number = fields.char(string="VIN Number")
    make = fields.char(string="Make")
    year = fields.char(string="Year")
    model = fields.char(string="Model")
    description = fields.char(string="Description")
    regitration_exp_date = fields.Date(string='Registration Expiration Date')
    use = fields.Selection(
        [('persolal', 'Personal'), ('comercial', 'Comercial'), ('both', 'Both')], default='comercial', string='Use')  
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'vehicle.details') or 'New'
        return super(VehicleDetails, self).create(vals)              