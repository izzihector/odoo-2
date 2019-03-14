# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree
import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    request_ids=fields.One2many('maintenance.request','ticket_id',u'Request')

    equipment_id=fields.Many2one('maintenance.equipment', u'Equipment')

    client_id = fields.Many2one('res.partner', related='equipment_id.client_id', string='Client', store=True, readonly=True)

