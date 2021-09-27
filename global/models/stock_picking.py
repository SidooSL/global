# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo import api, models, fields, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    receptor = fields.Char(string="Receptor Mercancía")
    receptor_email = fields.Char(string="Receptor Email")
    firma_cliente = fields.Binary(string="Firma cliente")

    def enviar_correo_albaran(self):
        # mail_template = self.env.ref('global.albaran_entragado_email')
        # mail_template.send_mail(self.id, force_send=True)
        # no confirmado stock.report_deliveryslip_copy_2_copy_1
        # confirmado: stock.report_deliveryslip_copy_2_copy_2
        # studio_customization.report_deliveryslip__203dd924-9a30-4f65-9fa4-d4edd029af56
        #report_template_id = self.env.ref('studio_customization.report_deliveryslip__203dd924-9a30-4f65-9fa4-d4edd029af56').sudo().render_qweb_template(self.id)

        #report_template = self.env['ir.actions.report']._get_report_from_name('stock.report_deliveryslip_copy_2_copy_1')

        report_template = self.env['ir.actions.report']._get_report_from_name('stock.report_deliveryslip_copy_3')
        report_template_data = report_template.sudo().render_qweb_pdf([int(self.id)])

        data_record = base64.b64encode(report_template_data[0])
        ir_values = {
            'name': "Albaran.pdf",
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/x-pdf',
        }
        data_id = self.env['ir.attachment'].create(ir_values)
        email_template_id = self.env.ref("global.albaran_entragado_email")
        email_template_id.attachment_ids = [(6, 0, [data_id.id])]

        email_to = self.partner_id.email

        if self.receptor_email:
            email_to = self.receptor_email

        email_values = {'email_to': email_to,
                        'email_from': self.env.user.email}

        email_template_id.send_mail(self.id, email_values=email_values, force_send=True)
        email_template_id.attachment_ids = [(3, data_id.id)]

        return {
            'warning': {
                'title': 'Email enviado',
                'message': 'El correo se ha enviado al destinatario: %s' % (email_to,)
            }
        }



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
