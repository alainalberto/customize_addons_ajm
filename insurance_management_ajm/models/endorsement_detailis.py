
from odoo import api, fields, models, _


class EndorsmentDetails(models.Model):
    _name = 'endorsment.details'

    name = fields.Char(string='Name', required=True, copy=False,
                       readonly=True, index=True, default=lambda self: _('New'))
    name_2 = fields.Char(
        string='Name 2', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    insurance_id = fields.Many2one('insurance.details', required=True,
                                   domain=[('state', '=', 'confirmed')],
                                   help="Confirmed orders can be selected")
    partner_id = fields.Many2one(related='insurance_id.partner_id',
                                 string='Customer', readonly=True)
    policy_id = fields.Many2one(related='insurance_id.policy_id',
                                string='Policy', readonly=True)
    employee_id = fields.Many2one('employee.details',
                                  string='Follow Up Person', required=True, defaul='insurance_id.employee_id' )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        inverse='_inverse_product_id',
        ondelete='restrict')
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    type = fields.Selection(
        [('gross', 'Gross'), ('monthly', 'Monthly'), ('net', 'Net')], 
        required=True, default='new', string='Type')
    transantion_type= fields.Selection(
        [('positive', 'Add'), ('negative', 'Remuve')], 
        required=True, default='positive', string='Transation Type')
    display_type = fields.Selection(
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
        compute='_compute_display_endorsment_type', store=True, readonly=False, precompute=True,
        required=True,
    )
    premium = fields.Float(string='Amount')
    down_payment = fields.Float(string='Down Payment')
    fee = fields.Float(string='Fee')
    commission_total = fields.Float(string='Commission Total')
    date_endorsment = fields.Date(
        string='Date Applied', default=fields.Date.context_today)
    invoice_id = fields.Many2one('account.move', string='Invoiced',
                                 readonly=True, copy=False)
    note_field = fields.Html(string='Comment')
    
    
    @api.depends('insurance_id')
    def _compute_display_endorsment_type(self):
        for line in self.filtered(lambda l: not l.display_type):
            
            )


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'endorsment.details') or 'New'
        return super(EndorsmentDetails, self).create(vals)

    def action_create_bill(self):
        if not self.invoice_id:
            invoice_val = self.env['account.move'].sudo().create({
                'move_type': 'in_invoice',
                'invoice_date': fields.Date.context_today(self),
                'partner_id': self.partner_id.id,
                'invoice_user_id': self.env.user.id,
                'endorsment_id': self.id,
                'invoice_origin': self.name,
                'invoice_line_ids': [(0, 0, {
                    'name': 'Invoice For Insurance Endorsment',
                    'quantity': 1,
                    'price_unit': self.premium,
                    'account_id': 41,
                })],
            })
            self.invoice_id = invoice_val