# partner_files/__manifest__.py
{
    'name': 'Client File Management',
    'version': '1.0',
    'summary': 'Management of client-related files',
    'category': 'Custom',
    'author': 'Alain Alberto',
    'website': 'http://www.simplytechsolution.com',
    'depends': ['base', 'contacts'],
    'qweb': [
        'static/src/xml/custom_template.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'static/src/xml/custom_template.xml'
        'views/files_partner_views.xml',
        'views/res_partner.xml',
        
    ],
    'assets': {
        'web.assets_backend': [
            'my_partner_files/static/src/js/custom_script.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}