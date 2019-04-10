# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class TechnicalSupportRequest(models.Model):
    _inherit = 'technical_support.request'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket')


class TechnicalSupportOrder(models.Model):
    _inherit = 'technical_support.order'

    tickets_id = fields.Many2one('helpdesk.ticket', string='Ticket')
