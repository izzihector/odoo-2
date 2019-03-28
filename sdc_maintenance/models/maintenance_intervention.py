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


class InterventionType(models.Model):
    _name = "intervention.type"
    _description = "type intervention"
    _order = 'name asc'

    name=fields.Char('Nom', required=True)
    code=fields.Char('Code')
    description=fields.Text('Description')
