
from odoo import models, fields

class PolicyDetails(models.Model):
    _name = 'policy.details'
    _description = 'Policy Details'

    name = fields.Char(string='New', required=True)
    policy_number = fields.Char(string="Policy Number",
                                   help="Policy number is a unique number that"
                                        "an insurance company uses to identify"
                                        "you as a policyholder")
    type_id = fields.Many2one(
        'policy.type', string='Policy Type', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ))
    team_id = fields.Many2one(
        comodel_name='crm.team',
        string="Sales Team",
        compute='_compute_team_id',
        store=True, readonly=False, precompute=True, ondelete="set null",
        change_default=True, check_company=True,  # Unrequired company
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    coverage_ids = fields.One2many('coverage.details', 'policy_id', string='Coverage')  
    endorsement_ids = fields.One2many('endorsement.details', 'policy_id', string='Endorsement')  
    invoice_id = fields.One2many(acount.move, string='Invoice')
    agency_id = fields.Many2one(
        'agency.details', string='Agency') 
    general_agency_id = fields.Many2one(
        'general.agency.details', string='General Agency') 
    carrier_id = fields.Many2one(
        'carrier.details', string='Carrier')
    mga = fields.Many2one(
        'mga.details', string='MGA')
    financial_id = fields.Many2one(
        'financial.details', string='Financial')
    status = fields.Selection(
        [('quotation', 'Quotation'), ('confirm', 'Confirm'), ('active', 'Active'), ('cancel', 'Cancel'), ('expire', 'Expire')], 
        required=True, default='gross', string='Transaction')
    start_date = fields.Date(string='Start Date')
    exp_date = fields.Date(string='Expiration Date')
    auto_renew = fields.Boolean(copy=False)
    bind_day = fields.Date(
        string='Bind Date', default=fields.Date.context_today)
    duration = fields.Integer(string='Duration in Days')
    premium = fields.Float(string='Premium')
    policy_total = fields.Float(string='Policy Total')
    down_payment = fields.Float(string='Down Payment')
    fee = fields.Float(string='Fee')
    commission_total = fields.Float(string='Commission Total')
    transaction = fields.Selection(
        [('new', 'New Policy'), ('renew', 'Renew Policy'), ('conciliation', 'Conciliation'), ('endorsement', 'Endorsement'), ('unear', 'Unear'), ('cancelation', 'Cancelation')], 
        required=True, default='new', string='Transaction') 
    binder_id = fields.Char( string='Binder ID', copy=False )
    policy_binder_invoice = fields.Char(string="Carrier Invoice Number" )
    
    policy_next_due = fields.Float(string='Next Due')
    policy_amount_financed = fields.Float(string='Amount Financed')
    policy_paid_mga = fields.Float(string='Paid MGA')
    
    

    
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
        self.state = 'active'
    
    def _compute_user_id(self):
        
        sale_order = self.env['sale.order']
        for record in self:
            record.user_id = sale_order._compute_user_id()

    def _compute_team_id(self):
        
        sale_order = self.env['sale.order']
        for record in self:
            record.user_id = sale_order._compute_team_id()

        

class PolicyType(models.Model):
    _name = 'policy.type'

    name = fields.Char(string='Name')

class CoverageDetails(models.Model):
    _name = 'coverage.details'

    name = fields.Char(string='Name')
    policy_id = fields.Many2one('policy.details', string='Policy')
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Policy Product",
        change_default=True, ondelete='restrict', check_company=True, index='btree_not_null',
        domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id), ('is_policy_pruduct', '=', True)]")
    coverage_type = fields.Selection(
        [('gross', 'Gross'), ('net', 'Net')], 
        required=True, default='gross', string='Coverage Type')
    coverage_amount = fields.Float(string='Coverage Amount')
    deductible = fields.Float(string='Deductible')
    premium = fields.Float(string='Premium')
    fee = fields.Float(string='Fee')
    commission = fields.Float(string='Commission')
    commission_rate = fields.Float(string='Commission Rate')
    commission_amount = fields.Float(string='Commission Amount')
    commission_paid = fields.Float(string='Commission Paid')
    commission_balance = fields.Float(string='Commission Balance')
    commission_date = fields.Date(string='Commission Date')
    commission_invoice = fields.Char(string='Commission Invoice')
    commission_paid_date = fields.Date(string='Commission Paid Date')
    commission_paid_invoice = fields.Char(string='Commission Paid Invoice')
    commission_paid_check = fields.Char(string='Commission Paid Check')
    commission_paid_amount = fields.Float(string='Commission Paid Amount')
    commission_paid_mga = fields.Float(string='Commission Paid MGA')
    commission_paid_agency = fields.Float(string='Commission Paid Agency')
    commission_paid_general_agency = fields.Float(string='Commission Paid General Agency')
    commission_paid_financial = fields.Float(string='Commission Paid Financial')
    commission_paid_employee = fields.Float(string='Commission Paid Employee')
    commission_paid_producer = fields.Float(string='Commission Paid Producer')
    commission_paid_subproducer = fields.Float(string='Commission Paid Subproducer')
    commission_paid_subproducer2 = fields.Float(string='Commission Paid Subproducer2')
    
class EndorsemntDetails(models.Model):
    _name = 'endorsement.details'

    name = fields.Char(string='Name')
    policy_id = fields.Many2one('policy.details', string='Policy')
    type = fields.Selection(
        selection=[
            ('initial', 'Initial Base Premium'),
            ('positive_add', 'Positive Endorsement Premium'),
            ('negative_add', 'Negative Emdosement Premium'),
            ('cancel', "Cancel"),
            ('renew', 'Renewal Premium'),
            ('rewrite', 'Rewrite Premium'),
            ('reinstate', 'Reinstante'),
            ('discount', 'General Discount'),
            ('govt', 'Govt Discount'),
            ('audit', 'Premiunm Audit'),
            ('credit', 'Credit'),
            ('installment', 'Installment Premium'),
            ('new', 'New Policy Premium'),
            ('no_impact', 'No Premium Impact'),
            ('other', 'Other')
        ],
        default = 'new',
        store=True, precompute=True,
        string='Type')
    endorsement_amount = fields.Float(string='Amount')
    down_payment = fields.Float(string='Down Payment')
    fee = fields.Float(string='Endorsement Fee')
    commission = fields.Float(string='Endorsement Commission')
    commission_rate = fields.Float(string='Endorsement Commission Rate')
    billing_status = fields.Selection(
        selection=[
            ('paid', 'Paid'),
            ('unpaid', 'Unpaid'),
            ('pending', 'Pending'),
            ('cancel', 'Cancel')
        ],
        default = 'unpaid',
        store=True, precompute=True,    
        string='Billing Status')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ))
    
    def _compute_user_id(self):
        
        sale_order = self.env['sale.order']
        for record in self:
            record.user_id = sale_order._compute_user_id()
        