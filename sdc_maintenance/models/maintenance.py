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

class maintenanceZone(models.Model):
    _name = 'maintenance.zone'
    _description = 'maintenance zone'
    _order = 'name asc'
    
    name=fields.Char('Zone',required=True)
    code=fields.Char('Reference de zone')
    manager_id=fields.Many2one('res.users','Responsible')
    
    description=fields.Text('Description')

class MaintenanceEquipmentBrand(models.Model):
    _name = 'maintenance.equipment.brand'
    _description = 'Brand'
    _order = 'name asc'
    
    name=fields.Char('Brand',required=True)
    code=fields.Char('Reference Brand')
    manager_id=fields.Many2one('res.partner','Provider')
    
    description=fields.Text('Description')

class MaintenanceSoftwareType(models.Model):
    _name = 'maintenance.software.type'
    _description = 'Software Type'
    _order = 'name asc'
    
    name=fields.Char('Software Type',required=True)
    code=fields.Char('Reference Software Type')
    
    description=fields.Text('Description')

class MaintenanceDicomType(models.Model):
    _name = 'maintenance.dicom.type'
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

class MaintenanceEquipmentSoftwareList(models.Model):
    _name = 'maintenance.equipment.software.list'
    _description = 'Software List'
    _order = 'name asc'
    
    name=fields.Char('License',required=True)

    software_id=fields.Many2one('maintenance.equipment.software','Software')
    equipment_id=fields.Many2one('maintenance.equipment','Equipment')
    
    description=fields.Text('Description')

class MaintenanceEquipmentSoftware(models.Model):
    _name = 'maintenance.equipment.software'
    _description = 'Software'
    _order = 'name asc'
    
    name=fields.Char('Software',required=True)
    version=fields.Char('Version')

    software_type_id=fields.Many2one('maintenance.software.type','Software Type')
    
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
    dicom_type_id=fields.Many2one('maintenance.dicom.type','Dicom Type')

    description=fields.Text('Description')
    
class ProductPiece(models.Model):
    _name = 'product.piece'
    _description = 'Spare Part'

    product_id=fields.Many2one('product.product', u'Spare Part',domain=[('is_piece','=',True)])
    ref_intern=fields.Char('Internal Reference')
    qte=fields.Integer('Amount')
    type_id=fields.Many2one('maintenance.piece','Piece Type')
    piece_id_equi=fields.Many2one('maintenance.equipment', u'Equipment')
    piece_id_intrv=fields.Many2one('maintenance.intervention', u'Intervention')
    piece_id_incid=fields.Many2one('maintenance.order', u'Work Order')


    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            product_obj = self.env['product.product'].browse(self.product_id.id)
            self.ref_intern = product_obj.default_code or False

class maintenancePiece(models.Model):
    _name = "maintenance.piece"
    _description = "maintenance piece"
    _order = 'name asc'

    name=fields.Char('Nom', required=True)
    code=fields.Char('Code')
    description=fields.Text('Description')

class maintenanceCritical(models.Model):
    _name = "maintenance.critical"
    _description = "critical"
    _order = 'name asc'

    name=fields.Char('Nom', required=True)
    code=fields.Char('Code')
    description=fields.Text('Description')
            

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

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_piece=fields.Boolean(u'Is Parts')

class MaintenanceEquipementCategory(models.Model):
    _inherit='maintenance.equipment.category'

    team_id=fields.Many2one('maintenance.team', u'Teams')
    helpdesk_team_id=fields.Many2one('helpdesk.team', u'Helpdesk Team')


class MaintenanceEquipementTeam(models.Model):
    _inherit='maintenance.team'

    team_leader_id=fields.Many2one('res.users', u'Team Leader')
    
class MaintenanceIntervention(models.Model):
    _name = "maintenance.intervention"
    _description = "Intervention Request"
    _order = "name desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
   

    @api.multi
    def archive_equipment_request(self):
        self.write({'archive': True})
                  
    @api.one
    def action_draft(self):
        self.state = 'draft'
        return True

    @api.one
    def action_cancel(self):
        self.state = 'cancel'
        return True

    @api.one
    def action_done(self):
        self.state = 'done'
        return True

    @api.one
    def action_process(self):
        self.state = 'process'
        return True       
        
    name=fields.Char('No. of intervention',readonly=True, default=lambda x: x.env['ir.sequence'].get('maintenance.intervention'))
    zone_id=fields.Many2one('maintenance.zone', u'Zone')
    equipment_id=fields.Many2one('maintenance.equipment', u'Equipment')  
    category_id = fields.Many2one('maintenance.equipment.category', related='equipment_id.category_id', string='Category', store=True, readonly=True) 
    partner=fields.Many2one('res.partner', u'Client',domain=[('customer','=',True)])
    warranty=fields.Boolean(u'Under Warranty')
    failure_type=fields.Many2one('maintenance.failure', u'Failure Type')
    contact=fields.Char(u'Contact')
    date_inter=fields.Datetime(u'For Intervention')
    date_end=fields.Datetime(u'Intervention Date')
        
    date=fields.Datetime('Date', default=datetime.today())
    user_id=fields.Many2one('res.users', u'Responsible', default=lambda self: self._uid)
    technician_id=fields.Many2one('res.users', u'Technician')
        
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    color = fields.Integer('Color Index')
    observation=fields.Text(u'Intervention Report')
    bon_bool=fields.Boolean(u'Work Order')
    motif=fields.Text('Motif')
    #notice=fields.Many2one('maintenance.order',u'Bon')
    product_ids=fields.One2many('product.piece','piece_id_intrv',u'Spare Part')
        
    type=fields.Many2one('intervention.type', string="Type of Intervention")
    state_machine=fields.Selection([('start','Working'),('stop','Stopped')],u'State on Demand')
    state=fields.Selection([('draft',u'New Request'),('process',u'In Progress'),('worko',u'Work Order'),('done',u'Done'),('cancel',u'Canceled')],u'Statut',track_visibility='always', default='draft')
    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
                                    string='Kanban State', required=True, default='normal', track_visibility='onchange')
    type_re=fields.Selection([('re',u'Reclamation'),('inter',u'Intervention'),('pm',u'Maintenance preventive'),('cm',u'Maintenance corrective'),('lot',u'Lot')],u'Resource type', default='inter')
    history_ids=fields.One2many('maintenance.history', 'intervention_id', u'Resources Allocated',ondelete='set null')
    reclamation=fields.Text('Objet de reclamation')

    sale_order_id=fields.Many2one('sale.order',u'Quotation')
    date_service=fields.Date(u'Date of commissioning')
    date_reception=fields.Date(u'Customer reception date')
        
    amount=fields.Float(u'Rate')
    devis_ok=fields.Boolean(u'invoiced')
    ot=fields.Char(u'N° OT',track_visibility='always')
    

    @api.onchange('equipment_id')
    def _equipement(self):
        equipement_id=self.env['maintenance.equipment'].browse(self.equipment_id.id)
        if equipement_id.warranty_func==True:
            self.warranty=True
        else:self.warranty=False
            
               
    @api.depends('bon_bool')
    def action_gererate_order(self):
        for object_inter in self:  
            if object_inter.bon_bool==False:
                test = object_inter.failure_type.name or '  '
                test_1 = object_inter.motif or '  '
                test_2 = object_inter.reclamation or '   '
                data ={
                                                                          'reference' : object_inter.name or False,
                                                                          'priority' : object_inter.priority or False,
                                                                          'reclamation' :test +'\n'+ test_1 +'\n'+ test_2 or False,
                                                                          'partner_id' : object_inter.partner and object_inter.partner.id or False,
                                                                          'zone_id' : object_inter.zone_id and object_inter.zone_id.id or False,
                                                                          'warranty' : object_inter.warranty or False,
                                                                          'interv_ok' : True,
                                                                          'type_id' : object_inter.type.id or False,
                                                                          'failure_type' : object_inter.failure_type.id or False,
                                                                          'technician_id' : object_inter.technician_id.id or False,
                                                                          'interv_id' : object_inter.id or False,
                                                                          'state_machine' : object_inter.state_machine or False,
                                                                          'user_id' : object_inter.user_id and object_inter.user_id.id or False,
                                                                          'equipment_id' : object_inter.equipment_id and object_inter.equipment_id.id or False,
                                                                          }
                obj_gen = self.env['maintenance.order'].create(data)
                ot = self.env['maintenance.order'].browse(obj_gen.id)
                ote = ot.name or False
                self.write({'ot' : ote})
                if object_inter.history_ids:
                        for object_line in object_inter.history_ids:
                                resources_line={
                                                  'incident_id' :obj_gen.id,
                                                  'name' : object_line.name or False,
                                                  'user_id' : object_line.user_id and object_line.user_id.id or False,
                                                  'date' : object_line.date or False,
                                                  'description' : object_line.description or False,
                                                  }
                                self.env['maintenance.history'].create(resources_line)
                                
                if object_inter.product_ids:
                        for r in object_inter.product_ids:
                                product_line={
                                                  'piece_id_incid' :obj_gen.id,
                                                  'product_id' :r.product_id.id,
                                                  'ref_intern' : r.ref_intern or False,
                                                  'qte' : r.qte  or False,
                                                  'type_id' : r.type_id and r.type_id.id or False,
                                                  }
                                self.env['product.piece'].create(product_line)
                
                object_inter.bon_bool=True
            else:
                raise exceptions.except_orm(u'Attention ', u'l\'ordre de travail est deja généré pour cette intervention !')
        return True


    def mail_notif(self):
            text_inter = u"""<div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: rgb(255, 255, 255); ">
                    <p>Bonjour %s </p>
                    <p>Nous vous informons que vous êtes attribué à l'intervention suivante : %s</p>
                    <br/>
                    <p>-----------------------------</p>
                    <p>Client  : %s </p>
                     <p>Equipement  : %s </p>
                    <p>Catégorie  : %s </p>
                    <p>Etat de l'equipement  : %s </p>
                    <p>Priorité  : %s </p>
                    <p>Date  : %s </p>
                    <p>Responsable  : %s </p>
                    <p>Motif  : %s </p>
                    <p>------------------------------</p>
                    <p> Service de maintenance</p>
                    </div>
                    """
            mail_content = text_inter %(
                                        self.technician_id.name or False,
                                        self.name or False,   
                                        self.partner.name or False, 
                                        self.equipment_id.name or False,  
                                        self.category_id.name or False,  
                                        self.state_machine or False,  
                                        self.priority or False,  
                                        self.date_end or False,
                                        self.user_id.name or False,
                                        self.motif or False,
                                        )
            
            main_content = {
                            'subject': _('Service de maintenance - Intervention N° : %s') % (self.name),
                            'author_id': self.env.user.user_id.id,
                            'body_html': mail_content,
                            'email_to': self.technician_id.login,
                        }
            self.env['mail.mail'].create(main_content).send()
            
            
                         
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.env['ir.sequence'].get('maintenance.intervention'),
            'bon_bool': False
        })
        return super(MaintenanceIntervention, self).copy(default)

class maintenanceFailure(models.Model):
    _name = "maintenance.failure"
    _description = "failure cause"
    _order = 'name asc'

    name=fields.Char('Failure type', required=True)
    code=fields.Char('Code')
    description=fields.Text('failure description')
    

class maintenanceHistory(models.Model):
    _name = "maintenance.history"
    _description = "order follow-up history"

    name=fields.Char(u'Object')
    hours=fields.Float(u'Duration')
    date=fields.Datetime(u'Date + Time', default=datetime.today())
    description=fields.Text(u'Description')
    incident_id=fields.Many2one('maintenance.order', u'Work Order')
    intervention_id=fields.Many2one('maintenance.intervention', u'Intervention')
    user_id=fields.Many2one('res.users', u'Member', default=lambda self:self._uid)
    


class maintenanceOrder(models.Model):
    _name = "maintenance.order"
    _description = "Order" 
    _order = "name desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

      
    @api.multi
    def action_print(self):
        return self.env.ref('sdc_maintenance.report_maintenance_incident').report_action(self)

    
    @api.one
    @api.depends('interv_id')
    def action_done(self):
        if self.interv_id:
            objet_inter = self.env['maintenance.intervention'].browse(self.interv_id.id)
            report=self.description
            objet_inter.write({'state' : 'done','observation' : report})
            return self.write({'state' : 'done'})


    @api.one
    def action_draft(self):
        self.state = 'plan'
        return True

    @api.one
    def action_process(self):
        self.state = 'draft'
        return True

    @api.one
    def action_cancel(self):
        self.state = 'cancel'
        return True       

    @api.one
    @api.depends('interv_id')
    def action_devis(self):
        if self.interv_id:
            objet_inter = self.env['maintenance.intervention'].browse(self.interv_id.id)
            report=self.description
            objet_inter.write({'state' : 'done','observation' : report})
            return self.write({'state' : 'invoice'})
        else:
            return self.write({'state' : 'invoice'})
    
    name=fields.Char(u'N° Work Order',readonly=True, default=lambda x: x.env['ir.sequence'].get('maintenance.order'))
    state=fields.Selection([('plan',u'Planned'),('draft',u'In Progress'),('invoice',u'Quote to Make'),('done',u'Done'),('cancel',u'Canceled')],u'Statut',track_visibility='always', default='plan')
    zone_id=fields.Many2one('maintenance.zone', u'Zone')
    partner_id=fields.Many2one('res.partner', u'Client',domain=[('customer','=',True)])
    equipment_id=fields.Many2one('maintenance.equipment', u'Equipment')
    category_id = fields.Many2one('maintenance.equipment.category', related='equipment_id.category_id', string='Catégorie', store=True, readonly=True) 
    warranty=fields.Boolean(u'Under warranty')
    type_id=fields.Many2one('intervention.type',u'Type of intervention')
    date=fields.Datetime(u'OT date', default=datetime.today())
    user_id=fields.Many2one('res.users', u'Responsible',default=lambda self: self._uid)   
    product_ids=fields.One2many('product.piece','piece_id_incid',u'List of Parts')
    history_ids=fields.One2many('maintenance.history', 'incident_id', u'Resources allocated',ondelete='set null')
    description=fields.Text(u'Report')
    reclamation=fields.Text(u'Description')
    devis_ok=fields.Boolean(u'Quotation')
    interv_id=fields.Many2one('maintenance.intervention',u'Source')
    cm_ok=fields.Boolean(u'cm ok')
    pm_ok=fields.Boolean(u'pm ok')
    interv_ok=fields.Boolean(u'interv ok')
    failure_type=fields.Many2one('maintenance.failure', u'Failure type')
    devis_track=fields.Char(u'N° de devis',track_visibility='always')      
    maintenance_id = fields.Many2one('maintenance.checklist.history', 'Control List')
    state_machine=fields.Selection([('start','Working'),('stop','Stopped')],u'State on Demand')
    
    technician_id=fields.Many2one('res.users', u'Technicien')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    color = fields.Integer('Color Index')
    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
                                    string='Kanban State', required=True, default='normal', track_visibility='onchange')
    
    
    _sql_constraints = [
        ('maintenance_order_model_uniq', 'unique (name)', u'la Référence de l\'ordere de mission doit être unique'),
    ]


    def mail_notif(self):
            text_inter = u"""<div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: rgb(255, 255, 255); ">
                    <p>Bonjour %s </p>
                    <p>Nous vous informons que vous êtes attribué à l'ordre de travail suivant : %s</p>
                    <br/>
                    <p>-----------------------------</p>
                    <p>Client  : %s </p>
                    <p>Equipement  : %s </p>
                    <p>Catégorie  : %s </p>
                    <p>Etat de l'equipement  : %s </p>
                    <p>Priorité  : %s </p>
                    <p>Date  : %s </p>
                    <p>Responsable  : %s </p>
                    <p>Motif  : %s </p>
                    <p>------------------------------</p>
                    <p> Service de maintenance</p>
                    </div>
                    """
            mail_content = text_inter %(
                                        self.technician_id.name or False,
                                        self.name or False,   
                                        self.partner_id.name or False, 
                                        self.equipment_id.name or False,  
                                        self.category_id.name or False,  
                                        self.state_machine or False,  
                                        self.priority or False,  
                                        self.date or False,
                                        self.user_id.name or False,
                                        self.reclamation or False,
                                        )
            
            main_content = {
                            'subject': _('Service de maintenance - Ordre de travail N° : %s') % (self.name),
                            'author_id': self.env.user.user_id.id,
                            'body_html': mail_content,
                            'email_to': self.technician_id.login,
                        }
            self.env['mail.mail'].create(main_content).send()
            
    @api.onchange('equipment_id')
    def onchange_equipement(self):
        if self.equipment_id:
            object_patrimoin=self.env['maintenance.equipment'].browse(self.equipment_id.id) 
            if object_patrimoin.warranty_func == True:
                self.warranty = True 
            else : self.warranty = False
    
 
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.env['ir.sequence'].get('maintenance.order')})
        return super(maintenanceOrder, self).copy(default)

    @api.multi
    def action_gererate_invoice(self):
        for object_inter in self:  
                if object_inter.partner_id:    
                    sale_order_id = self.env['sale.order'].create({ 'origin':object_inter.name or False,
                                                                    'note': 'OT-' + object_inter.description or False,
                                                                    'partner_id' : object_inter.partner_id and object_inter.partner_id.id or False,
                                                                    })
                    devis_obj = self.env['sale.order'].browse(sale_order_id.id)
                    devis = devis_obj.name or False
                    self.write({'devis_track' : devis})
                    if object_inter.product_ids:
                        for object_line in object_inter.product_ids:
                                sale_order_line={
                                                      'product_id' :object_line.product_id.id or False,
                                                      'name' : object_line.product_id.name or False,
                                                      'product_uom_qty' : object_line.qte,
                                                      'order_id' : sale_order_id.id,
                                                      }
                                print (sale_order_line)
                                self.env['sale.order.line'].create(sale_order_line)      
                    if sale_order_id:
                        product_id = self.env['product.product'].search([('product_tmpl_id', '=', object_inter.equipment_id.id)])
                        data ={
                                'product_id' :product_id.id or False,
                                'order_id' : sale_order_id.id,
                               }
                        self.env['sale.order.line'].create(data)
                        
                    object_inter.state = 'done'
                else : raise exceptions.except_orm(u'Attention !!', u'Veuillez choisir un client !')
        return True


class InterventionType(models.Model):
    _name = "intervention.type"
    _description = "type intervention"
    _order = 'name asc'
    
    name=fields.Char('Nom', required=True)
    code=fields.Char('Code')
    description=fields.Text('Description')
    

class maintenanceChecklistHistory(models.Model):
    _name="maintenance.checklist.history"
    _description= "Checklist History"
    _inherit = ['mail.thread']
    _order = 'name desc'
    
    @api.onchange('checklist_id')
    def onchange_checklist_id(self):
        if self.checklist_id:
            liste = self.env['maintenance.question'].search([('checklist_id', '=', self.id)])
            #enrs = self.env['maintenance.question'].name_get(liste)
            res = []
            for id, name in liste:
                obj = {'name': name}
                res.append(obj)
            return {'value':{'answers_ids': res}}

    
    @api.one
    def action_done(self):
        self.state='done'
        return True
    
    @api.one
    def action_confirmed(self):
        self.state='confirmed'
        return True
    
    @api.one
    def action_draft(self):
        self.state='draft'
        return True
    
      
    name=fields.Char("Nom", default=lambda x: x.env['ir.sequence'].get('maintenance.checklist.history'))
    zone_id=fields.Many2one('maintenance.zone',u'Zone')
    checklist_id=fields.Many2one('maintenance.checklist', 'Control List')
    answers_ids=fields.One2many("maintenance.answer.history","checklist_history_id","Answers")
    ot_ids=fields.One2many('maintenance.order','maintenance_id',"Work Order")
    date_planned=fields.Datetime("Scheduled date")
    date_end=fields.Datetime("End Date")
    category_id=fields.Many2one('maintenance.equipment.category', u'Category')
    user_id=fields.Many2one('res.users', 'Responsible')
    state=fields.Selection([('draft', 'Rough draft'), ('confirmed', 'confirmado'),('done', 'Done')], "Status",track_visibility='always', default='draft')

    
class maintenanceChecklist(models.Model):
    _name="maintenance.checklist"
    _description= "checklist"
    _order = 'sequence, id'
    
    name=fields.Char("Title", required=True)
    active=fields.Boolean("Active", default=1)
    planned_date=fields.Float("Expected Duration")
    sequence=fields.Integer('Sequence')
    description=fields.Text('Description')
    questions_ids=fields.One2many("maintenance.question","checklist_id","Questions")
    equipment_type=fields.Many2one('maintenance.equipment.category', u'Category')
   
    
    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        context = {}
        if not default.get('name'):
            default.update(name=("%s (copy)") % (self.name))
        res = super(maintenanceChecklist, self).copy(default)
        return res

CHOICE_MAINT = [
    ('fait','Made'),
    ('bon','Good'),
    ('mauvais','Bad'),
    ('inapplicable','Inapplicable')]
   
class maintenanceQuestionHistory(models.Model):
    _name="maintenance.answer.history"
    _description= "Answers"
    _order = 'sequence, id'
       
    name=fields.Char(u"Action à réaliser",required=True)
    sequence=fields.Integer('Sequence')
    checklist_history_id=fields.Many2one('maintenance.checklist.history', u'Control List')
    answer=fields.Selection(CHOICE_MAINT, u"State")
    detail=fields.Char(u"Detail")

class maintenanceQuestion(models.Model):
    _name = "maintenance.question"
    _description = "Question"
    _order = 'sequence'
    
    name=fields.Char("Question", required=True)
    sequence=fields.Integer('Sequence')
    checklist_id=fields.Many2one('maintenance.checklist', 'Control List', required=True)
    
    
    
class MaintenanceRequestt(models.Model):
    _inherit= 'maintenance.request'

    @api.one
    def _days_next_due(self):
            for record in self:
                if (record.meter == "days") and record.maintenance_type=="preventive" and record.days_last_done:
                    interval = dt.timedelta(days = record.days_interval)
                    last_done = str(record.days_last_done)
                    last_done = dt.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval
                    record.days_next_due = next_due.strftime("%Y-%m-%d")
                else:
                    record.days_next_due = False
            return True
    
    @api.one
    def _days_left(self):
            for record in self:
                if (record.meter == "days") and record.maintenance_type=="preventive" and record.days_last_done:
                    interval = dt.timedelta(days=record.days_interval)
                    last_done = str(record.days_last_done)
                    last_done = dt.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval
                    NOW = dt.datetime.now()
                    due_days = next_due - NOW
                    record.days_left = due_days.days
                else:
                    record.days_left = False
            return True
    
    @api.one
    def _get_state(self):
            for record in self:    
                if record.meter == u'days':
                    if record.days_left <= 0:
                        record.state = u'Outdated'
                    elif record.days_left <= record.days_warn_period:
                        record.state = u'Approach'
                    else:
                        record.state = u'OK'
            return True


    meter=fields.Selection([ ('days', 'Days')], u'Measure Unit', default='days')
    state_machine=fields.Selection([('start','Working'),('stop','Stopped')],u'State on demand', default='start')

    recurrent=fields.Boolean(u'Recurrent ?', help="Mark this option if PM is periodic")

    days_interval=fields.Integer(u'Interval (days)')  
    days_warn_period=fields.Integer('Date of alert')
    days_left=fields.Integer(compute='_days_left', string='Remaining days')

    days_last_done=fields.Date(u'Last maintenance')
    days_next_due=fields.Date(compute='_days_next_due', string='Next Maintenance')

    state=fields.Char(compute='_get_state', string='Status',track_visibility='always')

    motif=fields.Text('Reason')

    technician_user_id = fields.Many2one('res.users', string='Technicianss', track_visibility='onchange')

    equipment_id=fields.Many2one('maintenance.equipment', u'Equipment')

    partner_id=fields.Many2one('res.partner', u'Cliente',domain=[('customer','=',True)])

    client_id = fields.Many2one('res.partner', related='equipment_id.client_id', string='Clients', store=True, readonly=True)

    team_id = fields.Many2one('maintenance.team', related='equipment_id.category_id.team_id', string='Teams', store=True, readonly=True)

    team_leader_id = fields.Many2one('res.users', related='equipment_id.category_id.team_id.team_leader_id', string='Team Leader', store=True, readonly=True)
     
    timesheet_ids=fields.One2many('account.analytic.line','request_id',u'Timesheet')


    def mail_notif(self):
            text_inter = u"""<div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: rgb(255, 255, 255); ">
                    <p>Bonjour %s </p>
                    <p>Nous vous informons que vous êtes attribué à la maintenance suivante : %s</p>
                    <br/>
                    <p>-----------------------------</p>
                    <p>Client  : %s </p>
                    <p>Equipement  : %s </p>
                    <p>Catégorie  : %s </p>
                    <p>Etat de l'equipement  : %s </p>
                    <p>Priorité  : %s </p>
                    <p>Date  : %s </p>
                    <p>Responsable  : %s </p>
                    <p>Motif  : %s </p>
                    <p>------------------------------</p>
                    <p> Service de maintenance</p>
                    </div>
                    """
            mail_content = text_inter %(
                                        self.technician_user_id.name or False,
                                        self.name or False,   
                                        self.partner_id.name or False, 
                                        self.equipment_id.name or False,  
                                        self.category_id.name or False,  
                                        self.state_machine or False,  
                                        self.priority or False,  
                                        self.schedule_date or False,
                                        self.owner_user_id.name or False,
                                        self.motif or False,
                                        )
            
            main_content = {
                            'subject': _('Service de maintenance - maintenance N° : %s') % (self.name),
                            'author_id': self.env.user.user_id.id,
                            'body_html': mail_content,
                            'email_to': self.technician_user_id.login,
                        }
            self.env['mail.mail'].create(main_content).send()


            
            
    
