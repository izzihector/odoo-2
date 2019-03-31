# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 emsa (<http://www.electronicamedica.com>).
#
##############################################################################

from odoo import api, fields, models
from odoo import tools

STATE_COLOR_SELECTION = [
    ('0', 'Red'),
    ('1', 'Green'),
    ('2', 'Blue'),
    ('3', 'Yellow'),
    ('4', 'Magenta'),
    ('5', 'Cyan'),
    ('6', 'Black'),
    ('7', 'White'),
    ('8', 'Orange'),
    ('9', 'SkyBlue')
]

class equipment_state(models.Model):
    """
    Model for Equipment states.
    """
    _name = 'equipment.state'
    _description = 'State of equipment'
    _order = "sequence"

    STATE_SCOPE_TEAM = [
        ('0', 'Finance'),
        ('1', 'Warehouse'),
        ('2', 'Manufacture'),
        ('3', 'Maintenance'),
        ('4', 'Accounting')
    ]

    name = fields.Char('State', size=64, required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Used to order states.", default=1)
    state_color = fields.Selection(STATE_COLOR_SELECTION, 'State Color')
    team = fields.Selection(STATE_SCOPE_TEAM, 'Scope Team')

    def change_color(self):
        color = int(self.state_color) + 1
        if (color>9): color = 0
        return self.write({'state_color': str(color)})


class equipment_category(models.Model):
    _description = 'Equipment Tags'
    _name = 'equipment.category'

    name = fields.Char('Tag', required=True, translate=True)
    equipment_ids = fields.Many2many('equipment.equipment', id1='category_id', id2='equipment_id', string='Equipments')


class equipment_equipment(models.Model):
    """
    Equipments
    """
    _name = 'equipment.equipment'
    _description = 'Equipment'
    _inherit = ['mail.thread']

    def _read_group_state_ids(self, domain, read_group_order=None, access_rights_uid=None, team='3'):
        access_rights_uid = access_rights_uid or self.uid
        stage_obj = self.env['equipment.state']
        order = stage_obj._order
        # lame hack to allow reverting search, should just work in the trivial case
        if read_group_order == 'stage_id desc':
            order = "%s desc" % order
        # write the domain
        # - ('id', 'in', 'ids'): add columns that should be present
        # - OR ('team','=',team): add default columns that belongs team
        search_domain = []
        search_domain += ['|', ('team','=',team)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(search_domain, order=order, access_rights_uid=access_rights_uid)
        result = stage_obj.name_get(access_rights_uid, stage_ids)
        # restore order of the search
        result.sort(lambda x,y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))
        return result, {}

    def _read_group_finance_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '0')

    def _read_group_warehouse_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '1')

    def _read_group_manufacture_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '2')

    def _read_group_maintenance_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '3')

    def _read_group_accounting_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '4')

    CRITICALITY_SELECTION = [
        ('0', 'General'),
        ('1', 'Important'),
        ('2', 'Very important'),
        ('3', 'Critical')
    ]

    name = fields.Char('Equipment Name', size=64, required=True, translate=True)
    finance_state_id = fields.Many2one('equipment.state', 'State', domain=[('team','=','0')])
    warehouse_state_id = fields.Many2one('equipment.state', 'State', domain=[('team','=','1')])
    manufacture_state_id = fields.Many2one('equipment.state', 'State', domain=[('team','=','2')])
    maintenance_state_id = fields.Many2one('equipment.state', 'State', domain=[('team','=','3')])
    accounting_state_id = fields.Many2one('equipment.state', 'State', domain=[('team','=','4')])
    maintenance_state_color = fields.Selection(related='maintenance_state_id.state_color', selection=STATE_COLOR_SELECTION, string="Color", readonly=True)
    criticality = fields.Selection(CRITICALITY_SELECTION, 'Criticality')
    property_stock_equipment = fields.Many2one(
        'stock.location', "Equipment Location",
        company_dependent=True, domain=[('usage', 'like', 'equipment')],
        help="This location will be used as the destination location for installed parts during equipment life.")
    user_id = fields.Many2one('res.users', 'Assigned to', track_visibility='onchange')
    active = fields.Boolean('Active', default=True)
    equipment_number = fields.Char('Equipment Number', size=64)
    model = fields.Char('Model', size=64)
    serial = fields.Char('Serial no.', size=64)
    vendor_id = fields.Many2one('res.partner', 'Vendor')
    manufacturer_id = fields.Many2one('res.partner', 'Manufacturer')
    start_date = fields.Date('Start Date')
    purchase_date = fields.Date('Purchase Date')
    warranty_start_date = fields.Date('Warranty Start')
    warranty_end_date = fields.Date('Warranty End')
    image = fields.Binary("Image")
    image_small = fields.Binary("Small-sized image")
    image_medium = fields.Binary("Medium-sized image")
    category_ids = fields.Many2many('equipment.category', id1='equipment_id', id2='category_id', string='Tags')

    _group_by_full = {
        'finance_state_id': _read_group_finance_state_ids,
        'warehouse_state_id': _read_group_warehouse_state_ids,
        'manufacture_state_id': _read_group_manufacture_state_ids,
        'maintenance_state_id': _read_group_maintenance_state_ids,
        'accounting_state_id': _read_group_accounting_state_ids,
    }

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(equipment_equipment, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(equipment_equipment, self).write(vals)
