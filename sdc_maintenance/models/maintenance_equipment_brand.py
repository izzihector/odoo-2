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

AVAILABLE_PRIORITIES = [
    ('0','Basse'),
    ('1','Normal'),
    ('2','Urgent')
]


class MaintenanceEquipmentBrand(models.Model):
    _name = 'maintenance.equipment.brand'
    _description = 'Brand'
    _order = 'name asc'
    
    name=fields.Char('Brand',required=True)
    code=fields.Char('Reference Brand')
    manager_id=fields.Many2one('res.partner','Provider')
    
    description=fields.Text('Description')
    


            
            
    
