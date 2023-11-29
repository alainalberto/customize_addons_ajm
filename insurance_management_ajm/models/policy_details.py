
from odoo import models, fields, api, _
from odoo import models

class PolicyDetails(models.Model):
    _name = 'policy.details'
    _description = 'Policy Details'

    
    name = fields.Char(
        string='Policy Reference', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    policy_number = fields.Char(string="Policy Number",
                                   help="Policy number is a unique number that"
                                        "an insurance company uses to identify"
                                        "you as a policyholder")
    type_id = fields.Many2one(
        'policy.type', string='Policy Type', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    sale_ids = fields.One2many('sale.order', 'policy_id', string='Sale Orders')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,
        tracking=2,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False)]".format(
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
    invoice_id = fields.Many2one('acount.move', string='Invoice')
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
        required=True, default='quotation', string='Status')
    tag_display = fields.Char(string='Tags', value='INSURANCE', readonly=True)
    start_date = fields.Date(string='Start Date')
    exp_date = fields.Date(string='Expiration Date')
    auto_renew = fields.Boolean(copy=False)
    bind_day = fields.Date(
        string='Bind Date', default=fields.Date.context_today)
    duration = fields.Integer(string='Duration in Days')
    premium = fields.Float(string='Premium Base')
    premium_emdorsement = fields.Float(string='Premium Endorsement')
    policy_total = fields.Float(string='Policy Total')
    down_payment = fields.Float(string='Down Payment')
    fee = fields.Float(string='Agency Fee')
    commission_total = fields.Float(string='Commission Total')
    transaction = fields.Selection(
        [('new', 'New Policy'), ('renew', 'Renew Policy'), ('conciliation', 'Conciliation'), ('endorsement', 'Endorsement'), ('unear', 'Unear'), ('cancelation', 'Cancelation')], 
        required=True, default='new', string='Transaction') 
    binder_id = fields.Char( string='Binder ID', copy=False )
    policy_binder_invoice = fields.Char(string="Carrier Invoice Number" )
    
    policy_next_due = fields.Float(string='Next Due')
    policy_amount_financed = fields.Float(string='Amount Financed')
    policy_paid_mga = fields.Float(string='Paid MGA')
    files_ids = fields.One2many('partner.files', 'policy_id', string='Files')
    
    
    @api.model
    def create(self, vals):
        # Llamar al método original create
        record = super(PolicyDetails, self).create(vals)
        
        # Buscar o crear el tag 'Policy'
        policy_tag = self.env['crm.tag'].search([('name', '=', record.tag_display)], limit=1)
        if not policy_tag:
            policy_tag = self.env['crm.tag'].create({'name': record.tag_display})
        # Si el estado es 'quotation', crear un pedido de venta relacionado
        
        if record.status == 'quotation':
            status = 'draft'
        elif record.status == 'confirm':
            status = 'sent'
        elif record.status == 'active':
            status = 'sale'
            

        # Crear un pedido de venta y asignar el tag
        sale_order_vals = {
            'partner_id': record.partner_id.id,
            'state': status,
            'tag_ids': [(6, 0, [policy_tag.id])],
            'user_id': record.user_id.id if record.user_id else False,
            'team_id': record.team_id.id if record.team_id else False,
        }

        sale_order = self.env['sale.order'].create(sale_order_vals)

        # Guardar la referencia del pedido de venta en la póliza
        record.sale_ids = [sale_order.id]

        # Crear líneas de pedido de venta para cada cobertura
        for coverage in record.coverage_ids:
            line_vals = {
                'order_id': sale_order.id,
                'product_id': coverage.product_id.id,
                'product_uom_qty': 1,
                'price_unit': coverage.premium,
                'name': coverage.product_id.name,  # Descripción basada en el nombre del producto
                'product_uom': coverage.product_id.uom_id.id,  # UoM del producto
                
            }

            self.env['sale.order.line'].create(line_vals)
        
        # Crear líneas de pedido de venta para cada endoso
        if record.endorsement_ids:
            
            for endorsement in record.endorsement_ids:
                line_vals = {
                    'order_id': sale_order.id,
                    'product_id': endorsement.product_id.id,
                    'product_uom_qty': 1,
                    'price_unit': endorsement.endorsement_amount,
                    'name': endorsement.product_id.name,  # Descripción basada en el nombre del producto
                    'product_uom': endorsement.product_id.uom_id.id,  # UoM del producto
                    
                }

                self.env['sale.order.line'].create(line_vals)
        
        return record
    
    @api.model
    def update(self, vals):
        # Llamar al método original create
        record = super(PolicyDetails, self).update(vals)
        
        # Buscar o crear el tag 'Policy'
        policy_tag = self.env['crm.tag'].search([('name', '=', record.tag_display)], limit=1)
        if not policy_tag:
            policy_tag = self.env['crm.tag'].create({'name': record.tag_display})
        # Si el estado es 'quotation', crear un pedido de venta relacionado
        
        if record.status == 'quotation':
            status = 'draft'
        elif record.status == 'confirm':
            status = 'sent'
            

        # Crear un pedido de venta y asignar el tag
        sale_orders = self.env['sale.order'].search([('policy_id', '=', record.id)])
        sale_order_line = self.env['sale.order.line'].search([('order_id', '=', sale_orders.id)])
            
        if sale_order:
            sale_order_vals = {
                'partner_id': record.partner_id.id,
                'state': status,
                'tag_ids': [(6, 0, [policy_tag.id])],
                'user_id': record.user_id.id if record.user_id else False,
                'team_id': record.team_id.id if record.team_id else False,
            }
            sale_orders.write(sale_order_vals)
            for sale_order in sale_orders:
                if  record.coverage_ids:
                    for coverage in record.coverage_ids:
                        line_vals = {
                            'order_id': sale_order.id,
                            'product_id': coverage.product_id.id,
                            'product_uom_qty': 1,
                            'price_unit': coverage.premium,
                            'name': coverage.product_id.name,  # Descripción basada en el nombre del producto
                            'product_uom': coverage.product_id.uom_id.id,  # UoM del producto
                            
                        }
                        sale_order_line.write(line_vals)
                if record.endorsement_ids:        
                    for endorsement in record.endorsement_ids:
                        line = self.env['sale.order.line'].search([('order_id', '=', sale_order.id), ('product_id', '=', endorsement.product_id.id)])
                        if line:
                            line_vals = {
                                'order_id': sale_order.id,
                                'product_id': endorsement.product_id.id,
                                'product_uom_qty': 1,
                                'price_unit': endorsement.endorsement_amount,
                                'name': endorsement.product_id.name,  # Descripción basada en el nombre del producto
                                'product_uom': endorsement.product_id.uom_id.id,  # UoM del producto
                            }
                            sale_order_line.write(line_vals)
                        else:
                            policy_tag = self.env['crm.tag'].search([('name', '=', record.tag_display)], limit=1)
                            if not policy_tag:
                                policy_tag = self.env['crm.tag'].create({'name': record.tag_display})
                            if record.status == 'quotation':
                                status = 'draft'
                            elif record.status == 'confirm':
                                status = 'sent'
                            elif record.status == 'active':
                                status = 'sale'
                            sale_order_vals = {
                                'partner_id': record.partner_id.id,
                                'state': status,
                                'tag_ids': [(6, 0, [policy_tag.id])],
                                'user_id': record.user_id.id if record.user_id else False,
                                'team_id': record.team_id.id if record.team_id else False,
                            }

                            sale_order = self.env['sale.order'].create(sale_order_vals)
                            
                            for endorsement in record.endorsement_ids:
                                line_vals = {
                                    'order_id': sale_order.id,
                                    'product_id': endorsement.product_id.id,
                                    'product_uom_qty': 1,
                                    'price_unit': endorsement.endorsement_amount,
                                    'name': endorsement.product_id.name,  # Descripción basada en el nombre del producto
                                    'product_uom': endorsement.product_id.uom_id.id,  # UoM del producto
                                    
                                }

                                self.env['sale.order.line'].create(line_vals)
                            
            
        return record
    
    
    @api.constrains('policy_number')
    def _check_policy_number(self):
        if self.transaction != 'new':   
            if not self.policy_number:
                raise ValidationError(
                    _('Please add the policy number'))
                
            
    def action_active_insurance(self):
        for records in self.invoice_ids:
            if records.state == 'paid':
                self.state = 'active'
                raise UserError(_("All invoices must be paid"))
        
        self.efective_date = fields.Date.context_today(self)
        self.state = 'active'
    
    @api.depends('sale_ids')
    def _compute_user_id(self):
        for record in self:
            record.user_id = record.sale_ids[0].user_id if record.sale_ids else False

    @api.depends('sale_ids')
    def _compute_team_id(self):
        for record in self:
            record.team_id = record.sale_ids[0].team_id if record.sale_ids else False

        

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
        domain="[('sale_ok', '=', True), ('is_policy_product', '=', True)]")
    coverage_type = fields.Selection(
        [('gross', 'Gross'), ('net', 'Net')], 
        default='gross', string='Coverage Type')
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
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Policy Product",
        change_default=True, ondelete='restrict', check_company=True, index='btree_not_null',
        domain="[('sale_ok', '=', True), ('is_policy_product', '=', True)]")
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
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ))
    
    @api.depends('policy_id')
    def _compute_user_id(self):
        for record in self:
            record.user_id = record.policy_id.sale_ids[0].user_id if record.policy_id.sale_ids else False
        