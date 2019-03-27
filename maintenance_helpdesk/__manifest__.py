# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Helpdesk to Maintenance',
    'version': '1.1',
    "author": "Rocendo Tejada - Electronica Médica",
    'category': 'Hidden',
    'description': """
This module adds a shortcut the Maintenance in Helpdesk.
===========================================================================

This shortcut allows you to generate a Maintenance Request.

    """,
    'depends': ['helpdesk', 'maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_request_views.xml',
        'views/helpdesk_maintenance_templates.xml',
        'views/helpdesk_views.xml',
    ],
    'auto_install': True,
}
