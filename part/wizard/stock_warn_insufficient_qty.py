# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class StockWarnInsufficientQtyPart(models.TransientModel):
    _name = 'stock.warn.insufficient.qty.part'
    _inherit = 'stock.warn.insufficient.qty'
    _description = 'Warn Insufficient Part Quantity'

    part_id = fields.Many2one('part.order', string='Part')

    def action_done(self):
        self.ensure_one()
        return self.part_id.action_part_confirm()
