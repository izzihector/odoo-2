from ast import literal_eval
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    module_mail = fields.Boolean("Notifications")
    multi_company = fields.Boolean("Multi-societé")
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            multi_company=get_param('sdc_maintenance.multi_company'),
        )
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('sdc_maintenance.multi_company', self.multi_company)