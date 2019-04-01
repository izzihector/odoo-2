# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EquipmentModality(models.Model):
    _inherit = 'equipment.modality'

    team_id=fields.Many2one('helpdesk.team', string='Team')
