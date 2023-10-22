from odoo import models, fields, api

class InsuranceSale(models.Model):
    _name = 'insurance.sale'
    _description = 'Insurance Sales'

    name = fields.Char(string='Sale Reference', required=True)
    client_id = fields.Many2one('insurance.client', string='Client', required=True)
    policy_ids = fields.Many2many('insurance.policy', string='Insurance Policies')
    total_premium = fields.Float(string='Total Premium')
    # Otros campos relacionados con la venta, como fecha, estado, etc.

    # Método para confirmar la venta
    def confirm_sale(self):
        # Aquí agregar la lógica para confirmar la venta
        # Esto puede incluir la creación de facturas y otros cálculos necesarios
        return True