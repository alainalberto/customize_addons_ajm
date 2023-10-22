from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class InsuranceCarrier(models.Model):
    _inherit = 'res.partner'
    _name = 'insurance.carrier'
    # General
    fein = fields.Char(string='FEIN')
    sic = fields.Char(string='SIC')
    naic = fields.Char(string='NAIC')
    