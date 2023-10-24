# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class InsuranceDetails(models.Model):
    _name = 'insurance.details'

    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True)
    start_date = fields.Date(
        string='Start Date', default=fields.Date.context_today, required=True)
    efective_date = fields.Date(
        string='Efective Date')
    auto_renew = fields.Boolean(copy=False)
    bind_day = fields.Date(
        string='Bind Date', default=fields.Date.context_today)
    exp_date = fields.Date(string='Expiration Date', readonly=True)
    invoice_ids = fields.One2many('account.move', 'insurance_id',
                                  string='Invoices', readonly=True)
    #endorsement_id = fields.One2many( 
    #    'endorsement.details',
    #    'insurance_id',
    #    string='Policy lines',
    #    copy=False,
    #    readonly=True,
    #    domain=[('transantion_type', 'in', ('positive')), 'product_id', 'premium', 'down_payment','fee', 'employee_id'],
    #    states={'draft': [('readonly', False)]},
    #)

    employee_id = fields.Many2many(
        'hr.employee', string='Agent', required=True)
    commission_agents_id = fields.Many2many('hr.employee',
                                            domain=[('insurance_id', '=', self.id), ('employee_id', '=', self.employee_id)],  
                                            string='Agent Commission', 
                                            required=True)
    policy_id = fields.Many2one(
        'policy.details', string='Policy Type', required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    premium = fields.Float(string='Premium')
    policy_total = fields.Float(string='Policy Total')
    down_payment = fields.Float(string='Down Payment')
    fee = fields.Float(string='Fee')
    commission_total = fields.Float(string='Commission Total')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('active', 'Active')],
        required=True, default='draft')
    hide_inv_button = fields.Boolean(copy=False)
    note_field = fields.Html(string='Comment')
    policy_number = fields.Char(string="Policy Number", required=True,
                                   help="Policy number is a unique number that"
                                        "an insurance company uses to identify"
                                        "you as a policyholder")
    transaction = fields.Selection(
        [('new', 'New Policy'), ('renew', 'Renew Policy'), ('conciliation', 'Conciliation')], 
        required=True, default='new', string='Transaction')
    agency_id = fields.Many2one(
        'agency.details', string='Agency', required=True) 
    general_agency_id = fields.Many2one(
        'general.agency.details', string='General Agency', required=True) 
    carrier_id = fields.Many2one(
        'carrier.details', string='Carrier', required=True)
    mga = fields.Many2one(
        'mga.details', string='MGA', required=True)
    binder_id = fields.Char( string='Binder ID', copy=False )
    premium_sent = fields.Selection(
        [('gross', 'Gross'), ('monthly', 'Monthly'), ('net', 'Net')], 
        required=True, default='new', string='Transaction')
    binder_invoice = fields.Char(string="Carrier Invoice Number" )
    financial_id = fields.Many2one(
        'financial.details', string='Financial')
    net_due = fields.Float(string='Nex Due')
    amount_financed = fields.Float(string='Amount Financed')
    paid_mga = fields.Float(string='Paid MGA')
    
    
    
    

    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        if self.filtered(
                lambda reward: (
                        reward.commission_rate < 0 or reward.commission_rate > 100)):
            raise ValidationError(
                _('Commission Percentage should be between 1-100'))

    @api.constrains('policy_number')
    def _check_policy_number(self):
        if not self.policy_number:
            raise ValidationError(
                _('Please add the policy number'))

    def action_confirm_insurance(self):
        if self.premium > 0:
            self.state = 'confirmed'
            self.hide_inv_button = True
            sale = self.env['insurance.sale'].create({
            'name': self.name,  # Puedes personalizar cómo se genera el nombre de la venta
            'client_id': self.partner_id.id,
            'policy_ids': [(4, self.id)],
            'total_premium': self.premium,
            # Otros campos relacionados con la venta   
            })
            self.sale_id = sale
        else:
            raise UserError(_("Premium should be greater than zero"))

    def action_create_invoice(self):
        created_invoice = self.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.context_today(self),
            'partner_id': self.partner_id.id,
            'invoice_user_id': self.env.user.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': 'Invoice For Insurance Agency Fee',
                'quantity': 1,
                'price_unit': self.fee,
                'account_id': 41,
            })],
            'invoice_line_ids': [(1, 1, {
                'name': 'Invoice For Insurance Down Payment',
                'quantity': 1,
                'price_unit': self.down_payment,
                'account_id': 41,
            })],
        })
        self.invoice_ids = created_invoice
        if self.policy_id.payment_type == 'fixed':
            self.hide_inv_button = False

    def action_active_insurance(self):
        for records in self.invoice_ids:
            if records.state == 'paid':
                raise UserError(_("All invoices must be paid"))
        self.state = 'active'
        self.efective_date = fields.Date.context_today(self)
        self.hide_inv_button = False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'insurance.details') or 'New'
        return super(InsuranceDetails, self).create(vals)


class CommissionAgentDetails(models.Model):
    _name = 'commission.agent.details'
    
    insurance_id  = fields.Many2many('insurance.details', required=True)
    employee_id = fields.Many2many('hr.employee', required=True)
    commission_rate = fields.Float()
    total_commission = fields.Float()