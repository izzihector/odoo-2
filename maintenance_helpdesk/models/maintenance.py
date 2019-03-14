# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket')
