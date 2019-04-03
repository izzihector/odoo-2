# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime, timedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class EquipmentModality(models.Model):
    _inherit = 'equipment.modality'

    team_id=fields.Many2one('helpdesk.team', string='Team')
    team_leader_id=fields.Many2one('res.users', related='team_id.leader_id', string='Team Leader', store=True, readonly=True)

class EquipmentEquipment(models.Model):
    _inherit = 'equipment.equipment'

    team_id=fields.Many2one('helpdesk.team', related='modality_id.team_id', string='Team', store=True, readonly=True)
    team_leader_id=fields.Many2one('res.users', related='modality_id.team_id.leader_id', string='Team Leader', store=True, readonly=True)
