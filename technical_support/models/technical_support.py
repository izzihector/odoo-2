# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 emsa (<http://www.electronicamedica.com>).
#
##############################################################################

import time
from odoo import api, fields, models, _
from odoo import netsvc
import odoo.addons.decimal_precision as dp


class technical_support_order(models.Model):
    """
    Maintenance Orders
    """
    _name = 'technical_support.order'
    _description = 'Maintenance Order'
    _inherit =  ['mail.thread', 'mail.activity.mixin']

    STATE_SELECTION = [
        ('draft', 'DRAFT'),
        ('ready', 'IN PROCESS'),
        ('released', 'WAITING PARTS'),
        ('done', 'DONE'),
        ('cancel', 'CANCELED')
    ]

    MAINTENANCE_TYPE_SELECTION = [
        ('bm', 'Breakdown'),
        ('pm', 'Preventive'),
        ('cm', 'Corrective')
    ]

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'ready':
            return 'technical_support.mt_order_confirmed'
        return super(technical_support_order, self)._track_subtype(init_values)

    def _get_available_parts(self):
        for order in self:
            line_ids = []
            available_line_ids = []
            done_line_ids = []
            if order.procurement_group_id:
                for procurement in order.procurement_group_id.procurement_ids:
                    line_ids += [move.id for move in procurement.move_ids if move.location_dest_id.id == order.equipment_id.property_stock_equipment.id]
                    available_line_ids += [move.id for move in procurement.move_ids if move.location_dest_id.id == order.equipment_id.property_stock_equipment.id and move.state == 'assigned']
                    done_line_ids += [move.id for move in procurement.move_ids if move.location_dest_id.id == order.equipment_id.property_stock_equipment.id and move.state == 'done']
            order.parts_ready_lines = line_ids
            order.parts_move_lines = available_line_ids
            order.parts_moved_lines = done_line_ids

    name = fields.Char('Reference', size=64)
    origin = fields.Char('Source Document', size=64, readonly=True, states={'draft': [('readonly', False)]},
        help="Reference of the document that generated this maintenance order.")
    state = fields.Selection(STATE_SELECTION, 'Status', readonly=True, track_visibility='onchange',
        help="When the maintenance order is created the status is set to 'Draft'.\n\
        If the order is confirmed the status is set to 'Waiting Parts'.\n\
        If the stock is available then the status is set to 'Ready to Maintenance'.\n\
        When the maintenance is over, the status is set to 'Done'.", default='draft')
    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, readonly=True, states={'draft': [('readonly', False)]}, default='bm')
    description = fields.Char('Description', size=64, translate=True, required=True, readonly=True, states={'draft': [('readonly', False)]})

    date_planned = fields.Datetime('Planned Date', required=True, readonly=True, states={'draft':[('readonly',False)]}, default=time.strftime('%Y-%m-%d %H:%M:%S'), track_visibility='onchange')
    date_scheduled = fields.Datetime('Scheduled Date', required=True, readonly=True, states={'draft':[('readonly',False)],'released':[('readonly',False)],'ready':[('readonly',False)]}, default=time.strftime('%Y-%m-%d %H:%M:%S'), track_visibility='onchange')
    date_execution = fields.Datetime('Execution Date', required=True, states={'done':[('readonly',True)],'cancel':[('readonly',True)]}, default=time.strftime('%Y-%m-%d %H:%M:%S'), track_visibility='onchange')
    date_finish = fields.Datetime('Finish Date', required=True, states={'done':[('readonly',True)],'cancel':[('readonly',True)]}, default=time.strftime('%Y-%m-%d %H:%M:%S'), track_visibility='onchange')

    parts_lines = fields.One2many('technical_support.order.parts.line', 'maintenance_id', 'Planned parts',
        readonly=True, states={'draft':[('readonly',False)]})
    parts_ready_lines = fields.One2many('stock.move', compute='_get_available_parts')
    parts_move_lines = fields.One2many('stock.move', compute='_get_available_parts')
    parts_moved_lines = fields.One2many('stock.move', compute='_get_available_parts')

    tools_description = fields.Text('Tools Description',translate=True)
    labor_description = fields.Text('Labor Description',translate=True)
    operations_description = fields.Text('Operations Description',translate=True)
    documentation_description = fields.Text('Documentation Description',translate=True)
    problem_description = fields.Text('Problem Description')

    task_id = fields.Many2one('technical_support.task', 'Task', readonly=True, states={'draft': [('readonly', False)]})
    equipment_id = fields.Many2one('equipment.equipment', 'Equipment', required=True, readonly=True, states={'draft': [('readonly', False)]})
    user_id = fields.Many2one('res.users', 'Responsible', track_visibility='onchange', default=lambda self: self._uid)
    company_id = fields.Many2one('res.company','Company',required=True, readonly=True, states={'draft':[('readonly',False)]}, default=lambda self: self.env['res.company']._company_default_get('technical_support.order'))
    procurement_group_id = fields.Many2one('procurement.group', 'Procurement group', copy=False)
    category_ids = fields.Many2many(related='equipment_id.category_ids', string='equipment Category', readonly=True)
    wo_id = fields.Many2one('technical_support.workorder', 'Work Order', ondelete='cascade')
    request_id = fields.Many2one('technical_support.request', 'Request', readonly=True, states={'draft': [('readonly', False)]})
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]})

    client_id=fields.Many2one('res.partner', related='equipment_id.client_id', string='Client', store=True, readonly=True)
    brand_id=fields.Many2one('equipment.brand', related='equipment_id.brand_id', string='Brand', readonly=True)
    zone_id=fields.Many2one('equipment.zone', related='equipment_id.zone_id', string='Zone', readonly=True)
    model_id=fields.Many2one('equipment.model', related='equipment_id.model_id', string='Model', readonly=True)
    parent_id=fields.Many2one('equipment.equipment', related='equipment_id.parent_id', string='Equipment Relation', readonly=True)
    modality_id=fields.Many2one('equipment.modality', related='equipment_id.modality_id', string='Modality', readonly=True)


    _order = 'date_execution'

    @api.onchange('equipment_id','maintenance_type')
    def onchange_equipment(self):
        if self.equipment_id:
            self.category_ids = self.equipment_id.category_ids
        return {'domain': {'task_id': [('category_id', 'in', self.category_ids.ids),('maintenance_type','=',self.maintenance_type)]}}

    @api.onchange('date_planned')
    def onchange_planned_date(self):
        self.date_scheduled = self.date_planned

    @api.onchange('date_scheduled')
    def onchange_scheduled_date(self):
        self.date_execution = self.date_scheduled

    @api.onchange('date_execution')
    def onchange_execution_date(self):
        if self.state == 'draft':
            self.date_planned = self.date_execution
        else:
            self.date_scheduled = self.date_execution

    @api.onchange('task_id')
    def onchange_task(self):
        task = self.task_id
        new_parts_lines = []
        for line in task.parts_lines:
            new_parts_lines.append([0,0,{
                'name': line.name,
                'parts_id': line.parts_id.id,
                'parts_qty': line.parts_qty,
                'parts_uom': line.parts_uom.id,
                }])
        self.parts_lines = new_parts_lines
        self.description = task.name
        self.tools_description = task.tools_description
        self.labor_description = task.labor_description
        self.operations_description = task.operations_description
        self.documentation_description = task.documentation_description

    def test_ready(self):
        res = True
        for order in self:
            if order.parts_lines and order.procurement_group_id:
                states = []
                for procurement in order.procurement_group_id.procurement_ids:
                    states += [move.state != 'assigned' for move in procurement.move_ids if move.location_dest_id.id == order.equipment_id.property_stock_equipment.id]
                if any(states) or len(states) == 0: res = False
        return res

    def action_confirm(self):
        for order in self:
            order.write({'state':'ready'})
        return 0

    def action_ready(self):
        self.write({'state': 'released'})
        return True

    def action_done(self):
        self.write({'state': 'done', 'date_execution': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def ticket_done(self):
        for order in self:
            if order.ticket_id: order.ticket_id.write({'stage_id': 3})
        return True

    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True

    def test_if_parts(self):
        res = True
        for order in self:
            if not order.parts_lines:
                res = False
        return res

    def force_done(self):
        self.write({'state': 'done', 'date_execution': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def force_parts_reservation(self):
        self.write({'state': 'ready'})
        return True

    def _track_subtype(self, init_values):
        # init_values contains the modified fields' values before the changes
        #
        # the applied values can be accessed on the record as they are already
        # in cache
        self.ensure_one()
        if 'state' in init_values and self.state == 'done':
            return 'technical_support.mt_state_change'  # Full external id
        return super(technical_support_order, self)._track_subtype(init_values)

    @api.model
    def create(self, vals):
        if vals.get('name','/')=='/':
            vals['name'] = self.env['ir.sequence'].next_by_code('technical_support.order') or '/'
        return super(technical_support_order, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('date_execution') and not vals.get('state'):
            # constraint for calendar view
            for order in self:
                if order.state == 'draft':
                    vals['date_planned'] = vals['date_execution']
                    vals['date_scheduled'] = vals['date_execution']
                elif order.state in ('released','ready'):
                    vals['date_scheduled'] = vals['date_execution']
                else: del vals['date_execution']
        return super(technical_support_order, self).write(vals)


class technical_support_order_parts_line(models.Model):
    _name = 'technical_support.order.parts.line'
    _description = 'Maintenance Planned Parts'

    name = fields.Char('Description', size=64)
    parts_id = fields.Many2one('product.product', 'Parts', required=True)
    parts_qty = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    parts_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True)
    maintenance_id = fields.Many2one('technical_support.order', 'Maintenance Order')

    @api.onchange('parts_id')
    def onchange_parts(self):
        self.parts_uom = self.parts_id.uom_id

    def unlink(self):
        self.write({'maintenance_id': False})
        return True

    @api.model
    def create(self, values):
        ids = self.search([('maintenance_id','=',values['maintenance_id']),('parts_id','=',values['parts_id'])])
        if len(ids)>0:
            values['parts_qty'] = ids[0].parts_qty + values['parts_qty']
            ids[0].write(values)
            return ids[0]
        ids = self.search([('maintenance_id','=',False)])
        if len(ids)>0:
            ids[0].write(values)
            return ids[0]
        return super(technical_support_order_parts_line, self).create(values)


class technical_support_task(models.Model):
    """
    Maintenance Tasks (Template for order)
    """
    _name = 'technical_support.task'
    _description = 'Maintenance Task'

    MAINTENANCE_TYPE_SELECTION = [
        ('cm', 'Corrective')
    ]

    name = fields.Char('Description', size=64, required=True, translate=True)
    category_id = fields.Many2one('equipment.category', 'equipment Category', ondelete='restrict', required=True)
    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, default='cm')
    parts_lines = fields.One2many('technical_support.task.parts.line', 'task_id', 'Parts')
    tools_description = fields.Text('Tools Description',translate=True)
    labor_description = fields.Text('Labor Description',translate=True)
    operations_description = fields.Text('Operations Description',translate=True)
    documentation_description = fields.Text('Documentation Description',translate=True)
    active = fields.Boolean('Active', default=True)


class technical_support_task_parts_line(models.Model):
    _name = 'technical_support.task.parts.line'
    _description = 'Maintenance Planned Parts'

    name = fields.Char('Description', size=64)
    parts_id = fields.Many2one('product.product', 'Parts', required=True)
    parts_qty = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    parts_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True)
    task_id = fields.Many2one('technical_support.task', 'Maintenance Task')

    @api.onchange('parts_id')
    def onchange_parts(self):
        self.parts_uom = self.parts_id.uom_id.id

    def unlink(self):
        self.write({'task_id': False})
        return True

    @api.model
    def create(self, values):
        ids = self.search([('task_id','=',values['task_id']),('parts_id','=',values['parts_id'])])
        if len(ids)>0:
            values['parts_qty'] = ids[0].parts_qty + values['parts_qty']
            ids[0].write(values)
            return ids[0]
        ids = self.search([('task_id','=',False)])
        if len(ids)>0:
            ids[0].write(values)
            return ids[0]
        return super(technical_support_task_parts_line, self).create(values)


class technical_support_request(models.Model):
    _name = 'technical_support.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread']

    STATE_SELECTION = [
        ('draft', 'Draft'),
        ('claim', 'Claim'),
        ('run', 'Execution'),
        ('done', 'Done'),
        ('reject', 'Rejected'),
        ('cancel', 'Canceled')
    ]

    MAINTENANCE_TYPE_SELECTION = [
        ('bm', 'Breakdown'),
        ('pm', 'Preventive'),
        ('cm', 'Corrective')
    ]

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'claim':
            return 'technical_support.mt_request_sent'
        elif 'state' in init_values and self.state == 'run':
            return 'technical_support.mt_request_confirmed'
        elif 'state' in init_values and self.state == 'reject':
            return 'technical_support.mt_request_rejected'
        return super(technical_support_request, self)._track_subtype(init_values)

    name = fields.Char('Reference', size=64)
    state = fields.Selection(STATE_SELECTION, 'Status', readonly=True,
        help="When the maintenance request is created the status is set to 'Draft'.\n\
        If the request is sent the status is set to 'Claim'.\n\
        If the request is confirmed the status is set to 'Execution'.\n\
        If the request is rejected the status is set to 'Rejected'.\n\
        When the maintenance is over, the status is set to 'Done'.", track_visibility='onchange', default='draft')
    equipment_id = fields.Many2one('equipment.equipment', 'Equipment', required=True, readonly=True, states={'draft': [('readonly', False)]})
    cause = fields.Char('Subject', size=64, translate=True, required=True, readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    reject_reason = fields.Text('Reject Reason', readonly=True)
    requested_date = fields.Datetime('Requested Date', required=True, readonly=True, states={'draft': [('readonly', False)]}, help="Date requested by the customer for maintenance.", default=time.strftime('%Y-%m-%d %H:%M:%S'))
    execution_date = fields.Datetime('Execution Date', required=True, readonly=True, states={'draft':[('readonly',False)],'claim':[('readonly',False)]}, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    breakdown = fields.Boolean('Breakdown', readonly=True, states={'draft': [('readonly', False)]}, default=False)
    create_uid = fields.Many2one('res.users', 'Responsible')

    client_id=fields.Many2one('res.partner', related='equipment_id.client_id', string='Client', store=True, readonly=True)
    brand_id=fields.Many2one('equipment.brand', related='equipment_id.brand_id', string='Brand', readonly=True)
    zone_id=fields.Many2one('equipment.zone', related='equipment_id.zone_id', string='Zone', readonly=True)
    model_id=fields.Many2one('equipment.model', related='equipment_id.model_id', string='Model', readonly=True)
    parent_id=fields.Many2one('equipment.equipment', related='equipment_id.parent_id', string='Equipment Relation', readonly=True)
    modality_id=fields.Many2one('equipment.modality', related='equipment_id.modality_id', string='Modality', readonly=True)
    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, readonly=True, states={'draft': [('readonly', False)]}, default='bm')


    @api.onchange('requested_date')
    def onchange_requested_date(self):
        self.execution_date = self.requested_date

    @api.onchange('execution_date','state','breakdown')
    def onchange_execution_date(self):
        if self.state == 'draft' and not self.breakdown:
            self.requested_date = self.execution_date

    def action_send(self):
        value = {'state': 'claim'}
        for request in self:
            if request.breakdown:
                value['requested_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            request.write(value)

    def action_confirm(self):
        order = self.env['technical_support.order']
        order_id = False
        for request in self:
            order_id = order.create({
                'date_planned':request.requested_date,
                'date_scheduled':request.requested_date,
                'date_execution':request.requested_date,
                'origin': request.name,
                'state': 'draft',
                'maintenance_type': 'bm',
                'equipment_id': request.equipment_id.id,
                'description': request.cause,
                'problem_description': request.description,
                'request_id': request.id,
            })
        self.write({'state': 'run'})
        return order_id.id

    def action_done(self):
        self.write({'state': 'done', 'execution_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def action_reject(self):
        self.write({'state': 'reject', 'execution_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def action_cancel(self):
        self.write({'state': 'cancel', 'execution_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    @api.model
    def create(self, vals):
        if vals.get('name','/')=='/':
            vals['name'] = self.env['ir.sequence'].next_by_code('technical_support.request') or '/'
        return super(technical_support_request, self).create(vals)
