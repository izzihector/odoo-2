# -*- coding: utf-8 -*-
from odoo import http

# class HsSubscriptionsSync(http.Controller):
#	@http.route('/hs_subscriptions_sync/hs_subscriptions_sync/', auth='public')
#	def index(self, **kw):
#		return "Hello, world"

#     @http.route('/hs_subscriptions_sync/hs_subscriptions_sync/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hs_subscriptions_sync.listing', {
#             'root': '/hs_subscriptions_sync/hs_subscriptions_sync',
#             'objects': http.request.env['hs_subscriptions_sync.hs_subscriptions_sync'].search([]),
#         })

#     @http.route('/hs_subscriptions_sync/hs_subscriptions_sync/objects/<model("hs_subscriptions_sync.hs_subscriptions_sync"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hs_subscriptions_sync.object', {
#             'object': obj
#         })