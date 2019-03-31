﻿# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2018 emsa (<http://www.electronicamedica.com>).
#
##############################################################################

from odoo import api, fields, models, _

class technical_support_convert_order(models.TransientModel):
    _name = 'technical_support.convert.order'
    _description = 'Convert Order to Task'

    def convert_order(self):
        order_id = self._context.get('active_id', False)
        if order_id:
            order = self.env['technical_support.order'].browse(order_id)
            new_parts_lines = []
            for line in order.parts_lines:
                new_parts_lines.append([0,0,{
                    'name': line.name,
                    'parts_id': line.parts_id.id,
                    'parts_qty': line.parts_qty,
                    'parts_uom': line.parts_uom.id,
                    }])
            category_id = 1
            if order.equipment_id.category_ids:
                for category in order.equipment_id.category_ids:
                    category_id = category.id
                    break
            values = {
                'name': order.description,
                'category_id': category_id,
                'maintenance_type': order.maintenance_type if order.maintenance_type != 'bm' else 'cm',
                'parts_lines': new_parts_lines,
                'tools_description': order.tools_description,
                'labor_description': order.labor_description,
                'operations_description': order.operations_description,
                'documentation_description': order.documentation_description
            }
            return {
                'name': _('Task'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'technical_support.task',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.env['technical_support.task'].create(values).id,
            }
        return True
