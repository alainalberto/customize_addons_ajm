# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError




class ProductProduct(models.Model):
    _inherit = "product.product"

    is_policy_pruduct = fields.Boolean(copy=False , string='Is Policy Product')