# partner_files/__manifest__.py
{
    'name': 'Client File Management',
    'version': '1.0',
    'summary': 'Management of client-related files',
    'category': 'Custom',
    'author': 'Alain Alberto',
    'website': 'http://www.simplytechsolution.com',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/custom_template.xml',
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