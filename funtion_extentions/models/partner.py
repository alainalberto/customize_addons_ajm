
from odoo import api, fields, models, _


class ResPartner(models.Model):
     _inherit = "res.partner"

     x_cliente_ssn = fields.Char(string="Social Security Number", tracking=True)
     x_cliente_ein = fields.Char(string="EIN", tracking=True)
     x_cliente_usdot = fields.Char(string="US_DOT", tracking=True)
     x_cliente_pin = fields.Char(string="US_DOT Pin", tracking=True)
     x_cliente_user = fields.Char(string="US_DOT User", tracking=True)
     x_cliente_pasw = fields.Char(string="US_DOT Password", tracking=True)
     x_cliente_secut_quest = fields.Char(string="Security questions", tracking=True)
     x_cliente_mc = fields.Char(string="MC", tracking=True)
     x_cliente_tdmv = fields.Char(string="TDMV", tracking=True)
     x_cliente_login = fields.Char(string="Login", tracking=True)
     x_cliente_pass = fields.Char(string="Pass", tracking=True)
     x_cliente_uin = fields.Char(string="UIN", tracking=True)
     x_cliente_taxid = fields.Char(string="TaxID", tracking=True)
