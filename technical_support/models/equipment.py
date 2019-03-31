# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 emsa (<http://www.electronicamedica.com>).
#
##############################################################################

from odoo import api, fields, models, _


class EquipmentEquipment(models.Model):
    _name = 'equipment.equipment'
    _inherit = 'equipment.equipment'

    def _technical_support_count(self):
        maintenance = self.env['technical_support.order']
        for equipment in self:
            self.technical_support_count = maintenance.search_count([('equipment_id', '=', equipment.id)])

    def _next_maintenance(self):
        maintenance = self.env['technical_support.order']
        for equipment in self:
            order_ids = maintenance.search(
                [('equipment_id', '=', equipment.id),
                ('state', 'not in', ('done','cancel'))],
                limit=1, order='date_execution')
            if len(order_ids) > 0:
                self.maintenance_date = order_ids[0].date_execution

    technical_support_count = fields.Integer(compute='_technical_support_count', string='# Maintenance')
    maintenance_date = fields.Datetime(compute='_next_maintenance', string='Maintenance Date')

    def action_view_maintenance(self):
        return {
            'domain': "[('equipment_id','in',[" + ','.join(map(str, self.ids)) + "])]",
            'name': _('Maintenance Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'technical_support.order',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
