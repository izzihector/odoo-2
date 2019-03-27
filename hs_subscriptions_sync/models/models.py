# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class hs_subscriptions_sync(models.Model):
#     _name = 'hs_subscriptions_sync.hs_subscriptions_sync'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class SubscriptionsInvoiceSync(models.Model):
	_inherit = "account.invoice"


	@api.model
	def create(self, vals):
		override = super(SubscriptionsInvoiceSync, self).create(vals)
		self.search_subscriptions(override)
		return override


	def search_subscriptions(self, invoice):
		try:
			origin_name = invoice.origin
			if origin_name != False:
				subscription = self.env["sale.subscription"].search([('code', '=', origin_name)], limit=1)
				if len(subscription) != 0 :
					invoice.comment = subscription.description
		except:
			pass