# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo import api, models, fields, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    receptor = fields.Char(string="Receptor Mercancía")
    firma_cliente = fields.Binary(string="Firma cliente")

    # sign_request_ids = fields.Many2many('sign.request', string='Firmas')
    # sign_request_count = fields.Integer(compute='_compute_sign_request_count')
    #
    #
    # @api.depends('sign_request_ids')
    # def _compute_sign_request_count(self):
    #     for picking in self:
    #         picking.sign_request_count = len(picking.sign_request_ids)
    #
    # def open_sign_requests(self):
    #     self.ensure_one()
    #     if len(self.sign_request_ids.ids) == 1:
    #         return self.sign_request_ids.go_to_document()
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Firmas',
    #         'view_mode': 'kanban',
    #         'res_model': 'sign.request',
    #         'domain': [('id', 'in', self.sign_request_ids.ids)]
    #     }
