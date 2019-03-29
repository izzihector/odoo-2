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


class RegulatoryTechnicalFile(models.Model):
    _name = 'regulatory.technical.file'
    _description = 'Regulatory Technical File'

    name = fields.Char(string="Generic Name", required=True, translate=True)
    technical_file_number=fields.Char('Technical File Number')
    description=fields.Text('Description')
    group_id = fields.Many2one('regulatory.technical.file.group', string='Group')
    type_area_id = fields.Many2one('regulatory.technical.file.type.area', string='Type Area')


class RegulatoryTechnicalFileRegistry(models.Model):
    _name = 'regulatory.technical.file.registry'
    _description = 'Regulatory Technical File Registry'

    name = fields.Char(string="Proposed Name for the File", required=True, translate=True)
    technical_file_id = fields.Many2one('regulatory.technical.file', string='Technical File Number')
    observation=fields.Text('Observation')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    responsible_id = fields.Many2one('res.users', string='Responsible')


class RegulatoryTechnicalFileCreation(models.Model):
    _name = 'regulatory.technical.file.creation'
    _description = 'Regulatory Technical File Creation'

    name = fields.Char(string="Proposed Name for the File", required=True, translate=True)
    observation=fields.Text('Observation')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    responsible_id = fields.Many2one('res.users', string='Responsible')


class RegulatoryTechnicalFileModification(models.Model):
    _name = 'regulatory.technical.file.modification'
    _description = 'Regulatory Technical File Modification'

    name = fields.Char(string="Name of the Technical File", required=True, translate=True)
    technical_file_id = fields.Many2one('regulatory.technical.file', string='Technical File Number')
    observation=fields.Text('Description')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    responsible_sales_id = fields.Many2one('res.users', string='Responsible Sale')
