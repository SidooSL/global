# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from lxml import etree


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        param_obj = self.env['ir.config_parameter']
        res.update({'delivery_signature': param_obj.sudo().get_param('aspl_delivery_sign.delivery_signature')})
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param_obj = self.env['ir.config_parameter']
        param_obj.sudo().set_param('aspl_delivery_sign.delivery_signature', self.delivery_signature)

    delivery_signature = fields.Boolean("Require Signature")

class StokcPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        result = super(StokcPicking, self).button_validate()
        if self:
            config_sign = self.env['ir.config_parameter'].sudo().get_param('aspl_delivery_sign.delivery_signature')
            if config_sign and (not self.signature):
                raise UserError(_('Signature is required to make validate this picking.'))
        return result

    signature = fields.Binary("Signature", readonly=True)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(StokcPicking, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        config_sign = self.env['ir.config_parameter'].sudo().get_param('aspl_delivery_sign.delivery_signature')
        if config_sign and view_type == 'form':
            doc = etree.XML(res['arch'])
            if doc.xpath("//button[@name='signature_dummy']"):
                node = doc.xpath("//button[@name='signature_dummy']")[0]
                node.set('invisible', '0')
                modifiers = json.loads(node.get("modifiers"))
                modifiers['invisible'] = False
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: