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

    maintenance_ids = fields.One2many('technical_support.request', 'equipment_id')
    maintenance_count = fields.Integer(compute='_compute_maintenance_count', string="Maintenance Count", store=True)
    maintenance_open_count = fields.Integer(compute='_compute_maintenance_count', string="Current Maintenance", store=True)
    period = fields.Integer('Days between each Preventive maintenance')
    next_action_date = fields.Date(compute='_compute_next_maintenance', string='Date of the next preventive maintenance', store=True)
    maintenance_duration = fields.Float(help="Maintenance Duration in hours.")


    @api.depends('start_date', 'period', 'maintenance_ids.requested_date', 'maintenance_ids.close_date')
    def _compute_next_maintenance(self):
        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period > 0):
            next_maintenance_todo = self.env['technical_support.request'].search([
                ('equipment_id', '=', equipment.id),
                ('maintenance_type', '=', 'preventive'),
                ('state.done', '!=', True),
                ('close_date', '=', False)], order="requested_date asc", limit=1)
            last_maintenance_done = self.env['technical_support.request'].search([
                ('equipment_id', '=', equipment.id),
                ('maintenance_type', '=', 'preventive'),
                ('state.done', '=', True),
                ('close_date', '!=', False)], order="close_date desc", limit=1)
            if next_maintenance_todo and last_maintenance_done:
                next_date = next_maintenance_todo.requested_date
                date_gap = next_maintenance_todo.requested_date - last_maintenance_done.close_date
                # If the gap between the last_maintenance_done and the next_maintenance_todo one is bigger than 2 times the period and next request is in the future
                # We use 2 times the period to avoid creation too closed request from a manually one created
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period) * 2 and next_maintenance_todo.requested_date > date_now:
                    # If the new date still in the past, we set it for today
                    if last_maintenance_done.close_date + timedelta(days=equipment.period) < date_now:
                        next_date = date_now
                    else:
                        next_date = last_maintenance_done.close_date + timedelta(days=equipment.period)
            elif next_maintenance_todo:
                next_date = next_maintenance_todo.requested_date
                date_gap = next_maintenance_todo.requested_date - date_now
                # If next maintenance to do is in the future, and in more than 2 times the period, we insert an new request
                # We use 2 times the period to avoid creation too closed request from a manually one created
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period) * 2:
                    next_date = date_now + timedelta(days=equipment.period)
            elif last_maintenance_done:
                next_date = last_maintenance_done.close_date + timedelta(days=equipment.period)
                # If when we add the period to the last maintenance done and we still in past, we plan it for today
                if next_date < date_now:
                    next_date = date_now
            else:
                next_date = self.effective_date + timedelta(days=equipment.period)
            equipment.next_action_date = next_date

    @api.one
    @api.depends('maintenance_ids.state.done')
    def _compute_maintenance_count(self):
        self.maintenance_count = len(self.maintenance_ids)
        self.maintenance_open_count = len(self.maintenance_ids.filtered(lambda x: not x.state.done))
