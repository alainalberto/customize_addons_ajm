
{
    'name': 'Service Management AJM',
    'version': '1.0',
    'summary': 'Manage services for AJM company',
    'description': 'This module allows you to manage services for AJM company',
    'author': 'Your Name',
    'category': 'Uncategorized',
    'depends': ['base'],
    'data': [
        'views/service_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
