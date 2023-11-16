# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class EmployeeDetails(models.Model):
    _inherit = "hr.employee"

    
    
    salary_type = fields.Selection(
        [('fixed', 'Fixed'), ('commission', 'Commission'), ('both', 'Both')],
        default='commission', required=True)
    commission_rate = fields.Float(string='Commission Percentage')
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    base_salary = fields.Monetary(string='Base Salary')
    last_salary_date = fields.Date(string='Last Payment On', copy=False)
    note_field = fields.Html(string='Comment')
    invoice_id = fields.Many2one(
        'account.move', string='Last payment', copy=False, readonly=True)
    commission_ids = fields.One2many(
        'commission.employee', 'employee_id', string='Commissions')

    def action_salary_payment(self):
        if self.invoice_id:
            if self.invoice_id.state == 'draft':
                raise UserError(_("You must validate the last payment made in "
                                "order to create a new payment"))
        amount = 0.0
        if self.base_salary == 0.0:
            raise UserError(_("Amount should be greater than zero"))
        if self.salary_type == 'fixed':
            amount = self.base_salary
        elif self.salary_type == 'commission':
            for ins in self.insurance_ids:
                if self.last_salary_date:
                    if ins.start_date > self.last_salary_date:
                        amount += (ins.commission_rate * ins.amount) / 100
        else:
            amount = self.base_salary
            for ins in self.insurance_ids:
                if ins.start_date > self.last_salary_date:
                    amount += (ins.commission_rate * ins.amount) / 100
        invoice_date = self.env['account.move'].sudo().create({
            'move_type': 'in_invoice',
            'invoice_date': fields.Date.context_today(self),
            'partner_id': self.user_id.partner_id.id,
            'invoice_user_id': self.env.user.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': 'Invoice For Insurance Claim',
                'quantity': 1,
                'price_unit': amount,
                'account_id': 41,
            })],
        })
        self.sudo().write({
            'invoice_id': invoice_date.id,
            'last_salary_date': fields.Date.context_today(self),
        })

    @api.constrains('phone')
    def check_phone(self):
        """ make sure phone contains only valid characters"""
        for rec in self:
            if not re.match('^[0-9+\-() ]*$', rec.phone):
                raise ValidationError(
                    _('Only numbers, plus sign, hyphen, parentheses and spaces are permitted in phone number'))

class CommissionEmployee(models.Model):
    _name = 'commission.employee'
    
    sale_id  = fields.Many2many('sale.order')
    employee_id = fields.Many2many('hr.employee')
    commission_rate = fields.Float(string='Commission Percentage')
    invoice_id = fields.Many2one('account.move')
    periodo_start_date = fields.Date(string='Start Date')
    periodo_end_date = fields.Date(string='End Date')
    payment_date = fields.Date()
    total_commission = fields.Float()
    
    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        if self.filtered(
                lambda reward: (
                        reward.commission_rate < 0 or reward.commission_rate > 100)):
            raise ValidationError(
                _('Commission Percentage should be between 1-100'))
            
    @api.model
    def get_sales_by_employee_and_dates(self, employee_id, date_start, date_end):
        sales = self.env['sale.order'].search([
            ('employee_id', '=', employee_id),
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_end),
            ('state', 'in', ['sale', 'done']) # Only confirmed and paid sales
        ])
        return sales
    
    def button_filter_sales(self):
        self.ensure_one()
        sales = self.get_sales_by_employee_and_dates(self.employee_id.id, self.date_start, self.date_end)
        total_sales = sum(sale.amount_total for sale in sales)
        # Calcula el porcentaje aquí según tu lógica de negocio
        # percentage = ...   tu lógica de cálculo
        
    def action_commissions_payment(self):
        # Lógica para abrir la vista de pago de comisiones
        action = self.env.ref('view_commission_employee_form').read()[0]
        action['context'] = {
            'default_employee_id': self.id,  # Asegúrate de pasar el ID del empleado actual
            # Otras variables de contexto si son necesarias
        }
        return action