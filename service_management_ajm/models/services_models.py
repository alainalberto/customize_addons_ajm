from odoo import models, fields, api
from odoo import models, fields


class ServicesPartner(models.Model):
    _name = 'services.type'
    _description = 'Services Type'

    name = fields.Char(
        string='Permit Reference', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True) 


class ServicePermit(models.Model):
    _name = 'service.permit'
    _description = 'Permit'

    name = fields.Char(
        string='Permit Reference', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ))
    customers = fields.Many2one('res.partner', string='Customer', required=True)
    permit_type = fields.Selection([
        ('mc', 'MC'),
        ('usdot', 'USDOT'),
        ('txdmv', 'TXDMV'),
        ('boc3', 'BOC3'),
        ('ucr', 'UCR')
    ], string='Permit Type', required=True, multi=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    is_new = fields.Boolean(string='Is New', default=True)
    legal_status = fields.Char(string='Legal Status')
    business_type = fields.Char(string='Business Type')
    name = fields.Char(string='Name')
    attorney = fields.Char(string='Attorney')
    otheattorney = fields.Char(string='Other Attorney')
    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone')
    othephone = fields.Char(string='Other Phone')
    fax = fields.Char(string='Fax')
    ein = fields.Char(string='EIN')
    created_date = fields.Date(string='Created Date')
    unit = fields.Integer(string='Unit')
    usdot = fields.Integer(string='USDOT')
    usdot_pin = fields.Char(string='USDOT PIN')
    txdmv = fields.Char(string='TXDMV')
    txdmv_user = fields.Char(string='TXDMV User')
    txdmv_passd = fields.Char(string='TXDMV Password')
    txdmv_date = fields.Date(string='TXDMV Date')
    txdmv_date_exp = fields.Date(string='TXDMV Date Exp')
    mc = fields.Char(string='MC')
    mc_pin = fields.Char(string='MC PIN')
    ucr = fields.Boolean(string='UCR', default=False)
    ucr_date_exp = fields.Date(string='UCR Date Exp')
    account_number = fields.Char(string='Account Number')
    account_user = fields.Char(string='Account User')
    account_password = fields.Char(string='Account Password')
    inter = fields.Boolean(string='Inter', default=False)
    state = fields.Char(string='State')
    update = fields.Date(string='Update')
    deactivate = fields.Boolean(string='Deactivate', default=False)
    deactivate_date = fields.Date(string='Deactivate Date')
    boc3 = fields.Boolean(string='BOC3', default=False, required=lambda self: self.permit_type == 'boc3')
    boc3_date = fields.Date(string='BOC3 Date', required=lambda self: self.permit_type == 'boc3')


class ServiceIfta(models.Model):
    _name = 'service.ifta'
    _description = 'IFTA'

    name = fields.Char(
        string='Policy Reference', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ))
    customers = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Date(string='Date', default=fields.Date.today())
    ifta_type = fields.Char(string='Type')
    period = fields.Char(string='Period')
    nex_period = fields.Date(string='Next Period')
    paid = fields.Boolean(string='Paid', default=False)
    payment_due = fields.Date(string='Payment Due')
    state = fields.Char(string='State')
    update = fields.Date(string='Update')
