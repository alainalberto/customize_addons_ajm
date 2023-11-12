from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError

READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'sale', 'done', 'cancel'}
}

LOCKED_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'done', 'cancel'}
}

class SaleOrder(models.Model):
    """Inherits from 'sale.order' and adds custom fields and methods."""
    _inherit = 'sale.order'

    partner_shipping_id = fields.Many2one(
        comodel_name='res.partner',
        string="Delivery Address",
        compute='_compute_partner_shipping_id',
        store=True, readonly=False, required=False, precompute=True,
        states=LOCKED_FIELD_STATES,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string="Pricelist",
        compute='_compute_pricelist_id',
        store=True, readonly=False, precompute=True, check_company=True, required=False,  # Unrequired company
        states=READONLY_FIELD_STATES,
        tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected.")
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        store=True, precompute=True, ondelete="restrict")
    # Policy fields
    is_policy = fields.Boolean(copy=False, default=True, string='Policy Insurance')
    policy_start_date = fields.Date(
        string='Start Date', default=fields.Date.context_today, required=True)
    policy_efective_date = fields.Date(
        string='Efective Date')
    policy_auto_renew = fields.Boolean(copy=False)
    policy_bind_day = fields.Date(
        string='Bind Date', default=fields.Date.context_today)
    policy_exp_date = fields.Date(string='Expiration Date')
    policy_type_id = fields.Many2one(
        'policy.type', string='Policy Type', required=True)
    policy_duration = fields.Integer(string='Duration in Days')
    policy_premium = fields.Float(string='Premium')
    policy_total = fields.Float(string='Policy Total')
    policy_down_payment = fields.Float(string='Down Payment')
    policy_fee = fields.Float(string='Fee')
    policy_commission_total = fields.Float(string='Commission Total')
    policy_number = fields.Char(string="Policy Number",
                                   help="Policy number is a unique number that"
                                        "an insurance company uses to identify"
                                        "you as a policyholder")
    policy_transaction = fields.Selection(
        [('new', 'New Policy'), ('renew', 'Renew Policy'), ('conciliation', 'Conciliation')], 
        required=True, default='new', string='Transaction')
    policy_agency_id = fields.Many2one(
        'agency.details', string='Agency') 
    policy_general_agency_id = fields.Many2one(
        'general.agency.details', string='General Agency') 
    policy_carrier_id = fields.Many2one(
        'carrier.details', string='Carrier')
    policy_mga = fields.Many2one(
        'mga.details', string='MGA')
    policy_binder_id = fields.Char( string='Binder ID', copy=False )
    policy_premium_sent = fields.Selection(
        [('gross', 'Gross'), ('monthly', 'Monthly'), ('net', 'Net')], 
        required=True, default='gross', string='Transaction')
    policy_binder_invoice = fields.Char(string="Carrier Invoice Number" )
    policy_financial_id = fields.Many2one(
        'financial.details', string='Financial')
    policy_next_due = fields.Float(string='Next Due')
    policy_amount_financed = fields.Float(string='Amount Financed')
    policy_paid_mga = fields.Float(string='Paid MGA')
    display_tag_ids = fields.Char(compute='_compute_display_tag_ids')
    
    
    
    @api.constrains('policy_number')
    def _check_policy_number(self):
        if not self.policy_number:
            raise ValidationError(
                _('Please add the policy number'))
            
    
    def action_active_insurance(self):
        for records in self.invoice_ids:
            if records.state == 'paid':
                raise UserError(_("All invoices must be paid"))
        
        self.efective_date = fields.Date.context_today(self)

    @api.depends('is_policy')
    def _compute_display_tag_ids(self):
        for record in self:
            if record.is_policy:
                record.display_tag_ids = 'Policy'
            else:
                record.display_tag_ids = 'Service'

class PolicyType(models.Model):
    _name = 'policy.type'

    name = fields.Char(string='Name')