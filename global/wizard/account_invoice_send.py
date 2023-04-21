# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    def send_and_print_action(self):
        self.ensure_one()
        # Send the mails in the correct language by splitting the ids per lang.
        # This should ideally be fixed in mail_compose_message, so when a fix is made there this whole commit should be reverted.
        # basically self.body (which could be manually edited) extracts self.template_id,
        # which is then not translated for each customer.
        if self.composition_mode == 'mass_mail' and self.template_id:
            active_ids = self.env.context.get('active_ids', self.res_id)
            active_records = self.env[self.model].browse(active_ids)
            for record in active_records:
                lang = record.partner_id.lang
                self_record = self.with_context(
                    active_ids=record.ids,
                    active_id=record.id,
                    lang=lang,
                    default_res_id=record.id,
                    default_res_model='account.move',
                    mark_invoice_as_sent=True,
                    custom_layout="mail.mail_notification_paynow",
                    force_email=True)
                self_record.write({
                    'composition_mode': 'comment',
                    'template_id': self.template_id.id,
                    })
                self_record.onchange_template_id()
                self_record.partner_ids = record.partner_id
                self_record._send_email()
        else:
            self._send_email()
        if self.is_print:
            return self._print_document()
        return {'type': 'ir.actions.act_window_close'}

