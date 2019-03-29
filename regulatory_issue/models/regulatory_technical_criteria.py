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


class RegulatoryTechnicalCriteria(models.Model):
    _name = 'regulatory.technical.criteria'
    _description = 'Regulatory Technical Criteria'

    name = fields.Char(string="Certificate Name", required=True, translate=True)
    ctni=fields.Char('CTNI')
    technical_file=fields.Char('Technical File')
    criterion_expiration_date = fields.Date(u'Criterion Expiration Date')
    date_expiration_authenticated_seal = fields.Date(u'Date Expiration of the Authenticated Seal')
    description=fields.Text('Description')
