# -*- coding: utf-8 -*-
# Author : Rocendo Tejada
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

class MaintenanceEquipement(models.Model):
    _inherit = 'maintenance.equipment'

    @api.one
    @api.depends('intervention_ids')
    def _intervention_count(self):
        self.intervention_count = len(self.intervention_ids)        
                  
    @api.one 
    @api.depends('ot_ids')
    def _ot_count(self):
        self.ot_count = len(self.ot_ids)
    
    @api.one
    @api.depends('maintenance_ids.maintenance_type')
    def _pm_maintenance_count(self):
        self.pm_count = len(self.maintenance_ids.filtered(lambda x: x.maintenance_type=='preventive'))
        self.cm_count = len(self.maintenance_ids.filtered(lambda x: x.maintenance_type=='corrective'))

    @api.one
    def _days_waranty(self):
            for record in self:
                if record.deadlinegar:
                    fmt = '%Y-%m-%d'
                    d1 = date.today().strftime('%Y-%m-%d')
                    d2 = datetime.strptime(str(record.deadlinegar), fmt)
                    if d1 > d2.isoformat(): 
                        record.warranty_func = False
                    else:
                        record.warranty_func = True
                else:
                        record.warranty_func = True
            return True

    brand_id=fields.Many2one('maintenance.equipment.brand', u'Brand')

    team_id=fields.Many2one('maintenance.team', related='category_id.team_id', string='Teams', store=True, readonly=True)

    helpdesk_team_id=fields.Many2one('helpdesk.team', related='category_id.helpdesk_team_id', string='Helpdesk Team', store=True, readonly=True)

    team_leader_id=fields.Many2one('res.users', related='category_id.team_id.team_leader_id', string='Leader Team', store=True, readonly=True)

    zone_id=fields.Many2one('maintenance.zone', u'Zone')

    client_id=fields.Many2one('res.partner', string='Cliente', oldname="x_studio_cliente")

    model_id=fields.Many2one('maintenance.equipment.model', u'Models')

    parent_id=fields.Many2one('maintenance.equipment', u'Equipment Relation')

    product_ids=fields.One2many('product.piece','piece_id_equi',u'List of Parts')
 
    intervention_ids=fields.One2many('maintenance.intervention','equipment_id',u'Interventions')

    ot_ids=fields.One2many('maintenance.order','equipment_id',u'Work Order')    
 
    software_ids=fields.One2many('maintenance.equipment.software.list','equipment_id',u'Softwares')

    network_ids=fields.One2many('maintenance.equipment.network','equipment_id',u'Networks')

    dicom_ids=fields.One2many('maintenance.equipment.dicom','equipment_id',u'Dicom')

    child_ids=fields.One2many('maintenance.equipment','parent_id',u'Accesory')

    trademark=fields.Char(u'Marque')
    number_equipment=fields.Char(u'N°')

    technique_file=fields.Binary(u'Technical Sheet')
    image=fields.Binary(u'Image')

    startingdate=fields.Date(u"Date of commissioning")
    deadlinegar=fields.Date(u"End of warranty date")

    warranty_func=fields.Boolean(string='Under Warranty',compute='_days_waranty')
  

    safety=fields.Text(u'Security Instruction')

   
    ot_count=fields.Integer(compute='_ot_count',  string='OT')
    pm_count=fields.Integer(compute='_pm_maintenance_count', string='MP')
    cm_count=fields.Integer(compute='_pm_maintenance_count', string='MC')
    intervention_count=fields.Integer(compute='_intervention_count', string='Intervention', store=True)

    @api.model
    def _read_group_brand_ids(self, brands, domain, order):

        brand_ids = brands._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return brands.browse(brand_ids)
