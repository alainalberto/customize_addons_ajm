from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo import api, fields, models

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
        store=True, readonly=False, required=False,
        states=LOCKED_FIELD_STATES,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)  
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string="Pricelist",
        compute='_compute_pricelist_id',
        store=True, readonly=False, check_company=True, required=False,  # Unrequired company
        states=READONLY_FIELD_STATES,
        tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected.")
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id.id,
        store=True, ondelete="restrict")
    # Policy fields
    is_policy = fields.Boolean(
        string='Is Policy',
        store=True, readonly=False, required=False,
        states=LOCKED_FIELD_STATES)
    
    
    def open_policy_details(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Policy Details',
            'view_mode': 'tree',
            'res_model': 'policy.details',
            'domain': [('sale_id', '=', self.id)],
            'target': 'current',
        }