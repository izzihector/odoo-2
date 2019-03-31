# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 emsa (<http://www.electronicamedica.com>).
#
##############################################################################

from odoo import api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def write(self, vals):
        res = super(StockMove, self).write(vals)
        # from odoo import workflow
        # if vals.get('state') == 'assigned':
            # technical_support_obj = self.env['technical_support.order']
            # order_ids = technical_support_obj.search([('procurement_group_id', 'in', [x.group_id.id for x in self])])
            # for order_id in order_ids:
                # if order_id.test_ready():
                    # workflow.trg_validate(self.env.user.id, 'technical_support.order', order_id.id, 'parts_ready', self.env.cr)
        return res
