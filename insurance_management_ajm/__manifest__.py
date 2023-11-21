# -*- coding: utf-8 -*-
# Alain Alberto
{
    'name': 'Comercial Insurance Management',
    'version': '16.0.1.1.1',
    'summary': """Insurance Management & Operations""",
    'description': """Comercial Insurance Management for Agency""",
    'author': 'Alain Alberto',
    'company': 'Simply Tech Solution',
    'website': 'https://www.cybrosys.com',
    'category': 'Industries',
    'depends': ['account', 'base', 'sale', 'hr'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'data/insurance_management_data.xml',
        'views/employee_details_views.xml',
        'views/insurance_details_views.xml',
        'views/sale_order_views.xml',
        'views/insurance_management_menus.xml'
        
    ],
    'images': ['static/description/icon.svg'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
