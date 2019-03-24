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


class RegulatoryLegalDocumentationStage(models.Model):
    _name = 'regulatory.legal.documentation.stage'
    _description = 'Regulatory Legal Documentation Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Regulatory Legal Documentation Pipe')
    done = fields.Boolean('Request Done')


class RegulatoryLegalDocumentationType(models.Model):
    _name = 'regulatory.legal.documentation.type'
    _description = ' Regulatory Legal Documentation Type'
    _order = 'id'

    name = fields.Char(string="Type", required=True, translate=True)


class RegulatoryLegalDocumentation(models.Model):
    _name = 'regulatory.legal.documentation'
    _description = 'Regulatory Legal Documentation'
    _order = 'id'


    @api.returns('self')
    def _default_stage(self):
        return self.env['regulatory.legal.documentation.stage'].search([], limit=1)

    name = fields.Char(string="Legal Document", required=True, translate=True)
    apostille_number=fields.Char('Apostille Number')
    certificate_number=fields.Char('Certificate Number')
    expedition_date = fields.Date(u'Expedition Date')
    expiration_date = fields.Date(u'Expiration Date')
    description=fields.Text('Description')
    observation=fields.Text('Observation')
    type_id = fields.Many2one('regulatory.legal.documentation.type', u'Type')
    stage_id = fields.Many2one('regulatory.legal.documentation.stage', string='Stage', default=_default_stage)
