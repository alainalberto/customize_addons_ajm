# -*- coding: utf-8 -*-
#############################################################################
#
#    
#
#############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class FinancialDetails(models.Model):
    _name = 'financial.details'
    _description = 'Financial Details'
    
    
    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    email = fields.Char()
    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)


class AgencyDetails(models.Model):
    _name = 'agency.details'
    _description = 'Agency Details'
    
    
    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    parent_id = fields.Many2one('res.partner', string='Related Company', index=True)
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    email = fields.Char()
    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)
    
class GeneralAgencyDetails(models.Model):
    _name = 'general.agency.details'
    __description__ = 'General Agency Details'
    
    
    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    parent_id = fields.Many2one('res.partner', string='Related Company', index=True)
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    email = fields.Char()
    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)
    


class MGADetails(models.Model):
    _name = 'mga.details'
    _description = 'MGA Details'
    
    
    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    parent_id = fields.Many2one('res.partner', string='Related Company', index=True)
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    email = fields.Char()
    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)




class CarrierDetails(models.Model):
    _name = 'carrier.details'
    _description = 'Carrier Details'
    
    
    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    parent_id = fields.Many2one('res.partner', string='Related Company', index=True)
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    email = fields.Char()
    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)  
    naic_numbrer = fields.Integer(string='NAIC Number')
    
    
