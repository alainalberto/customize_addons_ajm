##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Marlon Falcon Hernandez
#    (<http://www.simplytechsolution.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'App AJM',
    'version': '16.0.1.0.0',
    'author': 'Alain Alberto Vinas',
    'maintainer': 'ALain Alberto Vinas',
    'website': 'http://www.simplytechsolution.com',
    'license': 'AGPL-3',
    'category': 'Extra Tools',
    'summary': 'Short summary.',
    'depends': ['account','base_setup', 'base', 'contacts'],
    'data': [
        'views/res_partner.xml',
        'views/webclient_templates.xml',
        'views/res_partner_views.xml',
        'views/customer_reference_view.xml',

     ],
    'assets': {
        'web.assets_backend_prod_only': [
            'funtion_extentions/static/src/js/favicon.js',
        ],
    },
    'images': [],

    

}