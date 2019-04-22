# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _, exceptions
import time
import datetime as dt
import time, datetime
from datetime import date
from datetime import datetime
from dateutil import relativedelta
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from dateutil.relativedelta import *

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _technical_support_count(self):
        maintenance = self.env['technical_support.order']
        for ticket in self:
            self.technical_support_count = maintenance.search_count([('ticket_id', '=', ticket.id)])

    request_ids=fields.One2many('technical_support.request','ticket_id', string='Requests')
    order_ids=fields.One2many('technical_support.order','ticket_id', string='Orders')

    client_id = fields.Many2one('res.partner', related='partner_id.commercial_partner_id', string='Cliente')

    equipment_id=fields.Many2one('equipment.equipment', u'Equipment')
    brand_id=fields.Many2one('equipment.brand', related='equipment_id.brand_id', string='Brand', readonly=True)
    zone_id=fields.Many2one('equipment.zone', related='equipment_id.zone_id', string='Zone', readonly=True)
    model_id=fields.Many2one('equipment.model', related='equipment_id.model_id', string='Model', readonly=True)
    parent_id=fields.Many2one('equipment.equipment', related='equipment_id.parent_id', string='Equipment Relation', readonly=True)
    modality_id=fields.Many2one('equipment.modality', related='equipment_id.modality_id', string='Modality', readonly=True)

    technical_support_count = fields.Integer(compute='_technical_support_count', string='# Reports')

    warranty_start_date = fields.Date('Warranty Start', related='equipment_id.warranty_start_date')
    warranty_end_date = fields.Date('Warranty End', related='equipment_id.warranty_end_date')
    dealer_warranty_start_date = fields.Date('Dealer Warranty Start', related='equipment_id.dealer_warranty_start_date')
    dealer_warranty_end_date = fields.Date('Dealer Warranty End', related='equipment_id.dealer_warranty_end_date')

    equipment_number = fields.Char('Equipment Number', related='equipment_id.equipment_number')
    serial = fields.Char('Serial no.', related='equipment_id.serial')
    location = fields.Char('Location', related='equipment_id.location')

    def action_confirm_main(self):
        order = self.env['technical_support.order']
        order_id = False
        for request in self:
            order_id = order.create({
                'date_planned':request.assign_date,
                'date_scheduled':request.assign_date,
                'date_execution':request.assign_date,
                'origin': request.id,
                'user_id': request.user_id.id,
                'state': 'draft',
                'maintenance_type': 'cm',
                'equipment_id': request.equipment_id.id,
                'description': request.name,
                'problem_description': request.description,
                'ticket_id': request.id,
            })
        self.write({'stage_id': 2})
        return order_id.id

    def action_view_report(self):
        return {
            'domain': "[('ticket_id','in',[" + ','.join(map(str, self.ids)) + "])]",
            'name': _('Maintenance Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'technical_support.order',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    leader_id=fields.Many2one('res.users', u'Leader')
