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

    request_ids=fields.One2many('technical_support.request','ticket_id', string='Request')
    equipment_id=fields.Many2one('equipment.equipment', u'Equipment')

    def action_confirm(self):
        order = self.env['technical_support.order']
        order_id = False
        for request in self:
            order_id = order.create({
                'date_planned':request.assign_date,
                'date_scheduled':request.assign_date,
                'date_execution':request.assign_date,
                'origin': request.id,
                'state': 'draft',
                'maintenance_type': 'bm',
                'equipment_id': request.equipment_id.id,
                'description': request.name,
                'problem_description': request.description
            })
        self.write({'stage_id': '2'})
        return order_id.id

class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    leader_id=fields.Many2one('res.users', u'Leader')
