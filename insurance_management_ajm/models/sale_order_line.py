from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    
    type = fields.Selection(
        [('gross', 'Gross'), ('monthly', 'Monthly'), ('net', 'Net')], 
        required=True, default='net', string='Type')
    transantion_type= fields.Selection(
        [('positive', 'Add'), ('negative', 'Remove')], 
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
        store=True, readonly=False, precompute=True,
        required=True,
    )
    down_payment = fields.Float(string='Down Payment')
    fee = fields.Float(string='Fee')
    date_endorsment = fields.Date(
        string='Date Applied', default=fields.Date.context_today)
