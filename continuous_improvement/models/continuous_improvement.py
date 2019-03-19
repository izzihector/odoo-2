# -*- coding: utf-8 -*-
###################################################################################
#
#    Electrónica Médica.
#    Copyright (C) 2019-TODAY Electrónica Médica (<https://www.electronicamedica.com>).
#
#    Author: Rocendo Tejada (<https://www.electronicamedica.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from datetime import date, datetime, timedelta
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError


class ContinuousImprovementStage(models.Model):
    _name = 'continuous.improvement.stage'
    _description = 'Continuous Improvement Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Maintenance Pipe')
    done = fields.Boolean('Request Done')

class ContinuousImprovementType(models.Model):
    _name = 'continuous.improvement.type'
    _description = ' Continuous Improvement Type'
    _order = 'id'

    name = fields.Char(string="Type", required=True, translate=True)


class ContinuousImprovement(models.Model):
    _name = 'continuous.improvement'
    _description = 'Continuous Improvement'
    _order = 'id'

    @api.returns('self')
    def _default_stage(self):
        return self.env['continuous.improvement.stage'].search([], limit=1)

    name = fields.Char(string="Asunto", required=True, translate=True)
    assigned_id = fields.Many2one('res.users', u'Assigned')
    type_id = fields.Many2one('continuous.improvement.type', u'Type')
    stage_id = fields.Many2one('continuous.improvement.stage', string='Stage', ondelete='restrict', track_visibility='onchange',
                               group_expand='_read_group_stage_ids', default=_default_stage)
    description=fields.Text('Description')
    observation=fields.Text('Observation')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)


