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


class RegulatoryTechnicalFileTypeArea(models.Model):
    _name = 'regulatory.technical.file.type.area'
    _description = 'Regulatory Technical File Type Area'

    name = fields.Char(string="Technical File Type Area", required=True, translate=True)
    description=fields.Text('Description')


class RegulatoryTechnicalFileGroup(models.Model):
    _name = 'regulatory.technical.file.group'
    _description = 'Regulatory Technical File Group'

    name = fields.Char(string="Technical File Group", required=True, translate=True)
    description=fields.Text('Description')


class RegulatoryTechnicalFileRegistryStage(models.Model):
    _name = 'regulatory.technical.file.registry.stage'
    _description = 'Regulatory Technical File Registry Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Regulatory Technical File Registry Pipe')
    done = fields.Boolean('Request Done')


class RegulatoryTechnicalFileCreationStage(models.Model):
    _name = 'regulatory.technical.file.creation.stage'
    _description = 'Regulatory Technical File Creation Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Regulatory Technical File Creation Pipe')
    done = fields.Boolean('Request Done')


class RegulatoryTechnicalFileModificationStage(models.Model):
    _name = 'regulatory.technical.file.modification.stage'
    _description = 'Regulatory Technical File Modification Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Regulatory Technical File Modification Pipe')
    done = fields.Boolean('Request Done')


class RegulatoryTechnicalFile(models.Model):
    _name = 'regulatory.technical.file'
    _description = 'Regulatory Technical File'
    _inherit = ['mail.thread']

    name = fields.Char(string="Generic Name", required=True)
    technical_file_number=fields.Char('Technical File Number')
    description=fields.Text('Description')
    group_id = fields.Many2one('regulatory.technical.file.group', string='Group')
    type_area_id = fields.Many2one('regulatory.technical.file.type.area', string='Type Area')


class RegulatoryTechnicalFileRegistry(models.Model):
    _name = 'regulatory.technical.file.registry'
    _description = 'Regulatory Technical File Registry'
    _inherit = ['mail.thread']

    @api.returns('self')
    def _default_stage(self):
        return self.env['regulatory.technical.file.registry.stage'].search([], limit=1)

    name = fields.Char(string="Proposed Name for the File", required=True, translate=True)
    technical_file_id = fields.Many2one('regulatory.technical.file', string='Technical File Number')
    observation=fields.Text('Observation')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    stage_id = fields.Many2one('regulatory.technical.file.registry.stage', string='Stage', default=_default_stage)


class RegulatoryTechnicalFileCreation(models.Model):
    _name = 'regulatory.technical.file.creation'
    _description = 'Regulatory Technical File Creation'
    _inherit = ['mail.thread']

    @api.returns('self')
    def _default_stage(self):
        return self.env['regulatory.technical.file.creation.stage'].search([], limit=1)

    name = fields.Char(string="Proposed Name for the File", required=True)
    observation=fields.Text('Observation')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    model_id = fields.Many2one('equipment.model', string='Model Equipment')
    stage_id = fields.Many2one('regulatory.technical.file.creation.stage', string='Stage', default=_default_stage)


class RegulatoryTechnicalFileModification(models.Model):
    _name = 'regulatory.technical.file.modification'
    _description = 'Regulatory Technical File Modification'
    _inherit = ['mail.thread']


    @api.returns('self')
    def _default_stage(self):
        return self.env['regulatory.technical.file.modification.stage'].search([], limit=1)

    name = fields.Char(string="Name of the Technical File", required=True)
    technical_file_id = fields.Many2one('regulatory.technical.file', string='Technical File Number')
    technical_file_name = fields.Char(related='technical_file_id.name', string='Technical File Name')
    observation=fields.Text('Description')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    responsible_sales_id = fields.Many2one('res.users', string='Responsible Sale')
    model_id = fields.Many2one('equipment.model', string='Model Equipment')
    stage_id = fields.Many2one('regulatory.technical.file.modification.stage', string='Stage', default=_default_stage)
