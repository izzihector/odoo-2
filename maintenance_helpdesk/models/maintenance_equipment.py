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


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    number_equipment=fields.Char(u'N°')


class MaintenanceEquipmentBrand(models.Model):
    _name = 'maintenance.equipment.brand'
    _description = 'Brand'
    _order = 'name asc'

    name=fields.Char('Brand',required=True)
    code=fields.Char('Reference Brand')
    manager_id=fields.Many2one('res.partner','Provider')
    description=fields.Text('Description')


class MaintenanceEquipmentSoftwareType(models.Model):
    _name = 'maintenance.equipment.software.type'
    _description = 'Software Type'
    _order = 'name asc'

    name=fields.Char('Software Type',required=True)
    code=fields.Char('Reference Software Type')
    description=fields.Text('Description')


class MaintenanceEquipmentZone(models.Model):
    _name = 'maintenance.equipment.zone'
    _description = 'Zone'
    _order = 'name asc'

    name=fields.Char('Zone',required=True)
    code=fields.Char('Reference de zone')
    manager_id=fields.Many2one('res.users','Responsible')
    description=fields.Text('Description')

class MaintenanceEquipmentDicomType(models.Model):
    _name = 'maintenance.equipment.dicom.type'
    _description = 'Dicom Type'
    _order = 'name asc'

    name=fields.Char('Dicom Type',required=True)
    code=fields.Char('Reference Dicom Type')
    description=fields.Text('Description')

class MaintenanceEquipmentModel(models.Model):
    _name = 'maintenance.equipment.model'
    _description = 'Model'
    _order = 'name asc'

    name=fields.Char('Model',required=True)
    code=fields.Char('Reference Model')
    brand_id=fields.Many2one('maintenance.equipment.brand','Brand')
    description=fields.Text('Description')


class MaintenanceEquipmentSoftware(models.Model):
    _name = 'maintenance.equipment.software'
    _description = 'Software'
    _order = 'name asc'

    name=fields.Char('Software',required=True)
    version=fields.Char('Version')

    software_type_id=fields.Many2one('maintenance.equipment.software.type','Software Type')

    description=fields.Text('Description')


class MaintenanceEquipmentSoftwareList(models.Model):
    _name = 'maintenance.equipment.software.list'
    _description = 'Software List'
    _order = 'name asc'

    name=fields.Char('License',required=True)
    software_id=fields.Many2one('maintenance.equipment.software','Software')
    equipment_id=fields.Many2one('maintenance.equipment','Equipment')
    description=fields.Text('Description')


class MaintenanceEquipmentNetwork(models.Model):
    _name = 'maintenance.equipment.network'
    _description = 'Network'
    _order = 'name asc'

    name=fields.Char('IP',required=True)
    subred=fields.Char('SubRed',required=True)
    gateway=fields.Char('Gateway',required=True)
    dns1=fields.Char('Dns1')
    dns2=fields.Char('Dns2')
    mac_address=fields.Char('Mac Address')
    equipment_id=fields.Many2one('maintenance.equipment','Equipment')
    description=fields.Text('Description')


class MaintenanceEquipmentDicom(models.Model):
    _name = 'maintenance.equipment.dicom'
    _description = 'Dicom'
    _order = 'name asc'

    name=fields.Char('AeTitle',required=True)
    ip=fields.Char('Ip',required=True)
    port=fields.Char('Port',required=True)
    equipment_id=fields.Many2one('maintenance.equipment','Equipment')
    dicom_type_id=fields.Many2one('maintenance.equipment.dicom.type','Dicom Type')
    description=fields.Text('Description')


class MaintenanceEquipementCategory(models.Model):
    _inherit='maintenance.equipment.category'

    team_id=fields.Many2one('maintenance.team', u'Teams')
    helpdesk_team_id=fields.Many2one('helpdesk.team', u'Helpdesk Team')


class MaintenanceEquipementTeam(models.Model):
    _inherit='maintenance.team'

    team_leader_id=fields.Many2one('res.users', u'Team Leader')
