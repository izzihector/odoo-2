# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Helpdesk to Technical Support',
    'version': '1.1',
    "author": "Rocendo Tejada - Electronica Médica",
    'category': 'Hidden',
    'description': """
This module adds a shortcut the Technical Support in Helpdesk.
===========================================================================

This shortcut allows you to generate a Technical Support Request.

    """,
    'depends': ['helpdesk', 'technical_support', 'equipment'],
    'data': [
        'views/technical_support_request_views.xml',
        'views/helpdesk_technical_support_templates.xml',
        'views/helpdesk_views.xml',
        'views/equipment_views.xml',
    ],
    'auto_install': True,
}
