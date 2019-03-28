# -*- coding: utf-8 -*-
# Author : Addi Ait-Mlouk
{
    "name": "Soporte Técnico",
    "version": "5.3",
    "depends": ['maintenance', "mail","sale",'website'],
    "author": "Rocendo Tejada - Electronica Médica",
    'website': 'https://www.electronicamedica.com/',
    'sequence':1,
    "category": "Productivity",
    'icon': '/sdc_maintenance/static/src/img/icon.png',
    'summary' : 'cmms, maintenance, Equipment, Repair, Machine, Corrective maintenance, Preventive maintenance, Intervention, Checklist, Work order, website',
    "description": """
        Open maintenance management system module allow you to manage 
        preventives and corrective maintenance without limit.
        All informations is linked to the equipment tree and let you follow 
        maintenance operation :
         - Repair.
         - Check up List.
         -

""",

    'data': [
        'data/maintenance_sequence.xml',
        'views/maintenance_views.xml',
        'views/maintenance_request_views.xml',
        'views/maintenance_equipment_views.xml',
        'views/maintenance_intervention_views.xml',
        'views/config_settings_views.xml',
        'views/error_template.xml',
        'views/succes_template.xml',
        'views/website_templates.xml',
        'controllers/intervention.xml',
        'controllers/pm.xml',
        'controllers/cm.xml',
        'controllers/wo.xml',
        'report/wo_template.xml',
        'report/cm_template.xml',
        'report/pm_template.xml',
        'report/intervention_template.xml',
        'report/equipment_template.xml',
        'report/report_menu.xml',
        'maintenance_menu.xml',
        'security/cmms_security.xml',
        'security/ir.model.access.csv'
    ],
    'images': ['static/description/thumb.jpg'],
    'demo_xml': [],
    'installable': True,
    'Aplication': True,
    'active': False,
}
