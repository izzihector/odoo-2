# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 emsa (<http://www.electronicamedica.com>).
#
##############################################################################

from odoo import api, fields, models
from odoo import netsvc

class technical_support_request_reject(models.TransientModel):
    _name = 'technical_support.request.reject'
    _description = 'Reject Request'

    reject_reason = fields.Text('Reject Reason', required=True)

    def reject_request(self):
        active_id = self._context.get('active_id')
        if active_id:
            request = self.env['technical_support.request'].browse(self._context.get('active_id'))
            request.write({'reject_reason':self.reject_reason})
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(self.env.user.id, 'technical_support.request', active_id, 'button_reject', self.env.cr)
        return {'type': 'ir.actions.act_window_close',}
