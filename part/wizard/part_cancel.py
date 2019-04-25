# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import UserError


class PartCancel(models.TransientModel):
    _name = 'part.cancel'
    _description = 'Cancel Part'

    @api.multi
    def cancel_part(self):
        if not self._context.get('active_id'):
            return {'type': 'ir.actions.act_window_close'}
        part = self.env['part.order'].browse(self._context['active_id'])
        if part.invoiced or part.invoice_method == 'none':
            part.action_cancel()
        else:
            raise UserError(_('Part order is not invoiced.'))
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(PartCancel, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
        part_id = self._context.get('active_id')
        if not part_id or self._context.get('active_model') != 'part.order':
            return res

        part = self.env['part.order'].browse(part_id)
        if not part.invoiced:
            res['arch'] = """
                <form string="Cancel Part">
                    <header>
                        <button name="cancel_part" string="_Yes" type="object" class="btn-primary"/>
                        <button string="Cancel" class="btn-secondary" special="cancel"/>
                    </header>
                    <label string="Do you want to continue?"/>
                </form>
            """
        return res
