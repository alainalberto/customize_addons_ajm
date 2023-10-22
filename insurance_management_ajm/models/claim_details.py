
from odoo import api, fields, models, _


class ClaimDetails(models.Model):
    _name = 'claim.details'

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
    employee_id = fields.Many2one('hr.employee',
                                  string='Agent', readonly=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    premium = fields.Float(string='Premium')
    date_claimed = fields.Date(
        string='Date Applied', default=fields.Date.context_today)
    invoice_id = fields.Many2one('account.move', string='Invoiced',
                                 readonly=True, copy=False)
    note_field = fields.Html(string='Comment')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'claim.details') or 'New'
        return super(ClaimDetails, self).create(vals)

    def action_create_bill(self):
        if not self.invoice_id:
            invoice_val = self.env['account.move'].sudo().create({
                'move_type': 'in_invoice',
                'invoice_date': fields.Date.context_today(self),
                'partner_id': self.partner_id.id,
                'invoice_user_id': self.env.user.id,
                'claim_id': self.id,
                'invoice_origin': self.name,
                'invoice_line_ids': [(0, 0, {
                    'name': 'Invoice For Insurance Cancelation',
                    'quantity': 1,
                    'price_unit': self.premium,
                    'account_id': 41,
                })],
            })
            self.invoice_id = invoice_val
