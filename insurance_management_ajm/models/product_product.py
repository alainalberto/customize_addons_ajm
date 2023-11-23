# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError




class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_policy_product = fields.Boolean(copy=False , string='Is Policy Product', default=True)