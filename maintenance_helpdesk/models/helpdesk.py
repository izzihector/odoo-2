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

    request_ids=fields.One2many('maintenance.request','ticket_id', string='Request')

    equipment_id=fields.Many2one('maintenance.equipment', u'Equipment')

    pm_count=fields.Integer(compute='_pm_maintenance_count', string='MP')
    cm_count=fields.Integer(compute='_pm_maintenance_count', string='MC')

    @api.one
    @api.depends('request_ids.maintenance_type')
    def _pm_maintenance_count(self):
        self.pm_count = len(self.request_ids.filtered(lambda x: x.maintenance_type=='preventive'))
        self.cm_count = len(self.request_ids.filtered(lambda x: x.maintenance_type=='corrective'))