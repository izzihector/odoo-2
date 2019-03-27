# -*- coding: utf-8 -*-
{
	'name': "Subscripciones sincronizadas",

	'summary': """
		Sincronizacion subscripciones-facturas""",

	'description': """
		Este modulo Corrige el comportamiento de Odoo al generar una factura 
		Borrado desde el modulo de suscripciones, Permitiendo asi que el campo
		Comentarios sea actualizado en la factura desde Suscripciones.
	""",

	'author': "HS Consulting S.A.",
	'website': "http://www.hconsul.com/odoo/",

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
	# for the full list
	'category': 'Sales',
	'version': '1.0',

	# any module necessary for this one to work correctly
	'depends': ['base', 'account', 'sale_subscription'],

	# always loaded
	'data': [
		# 'security/ir.model.access.csv',
		'views/views.xml',
		'views/templates.xml',
	],
	# only loaded in demonstration mode
	'demo': [
		'demo/demo.xml',
	],
}