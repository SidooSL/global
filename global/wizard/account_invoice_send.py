# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, format_date, get_lang



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
                template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
                lang = get_lang(self.env)
                if template and template.lang:
                    lang = template._render_template(template.lang, 'account.move', record.id)
                else:
                    lang = lang.code
                compose_form = self.env.ref('account.account_invoice_send_wizard_form', raise_if_not_found=False)
                ctx = dict(
                    default_model='account.move',
                    default_res_id=record.id,
                    # For the sake of consistency we need a default_res_model if
                    # default_res_id is set. Not renaming default_model as it can
                    # create many side-effects.
                    default_res_model='account.move',
                    default_use_template=bool(template),
                    default_template_id=template and template.id or False,
                    default_composition_mode='comment',
                    mark_invoice_as_sent=True,
                    custom_layout="mail.mail_notification_paynow",
                    # model_description=self.with_context(lang=lang).type_name,
                    force_email=True
                )
                new = self.with_context(ctx).copy({
                    'composition_mode': 'comment',
                    'res_id': record.id,
                    'invoice_ids': [(6, 0, [record.id])],
                    })
                new.composer_id.send_mail()
                if self.env.context.get('mark_invoice_as_sent'):
                    #Salesman send posted invoice, without the right to write
                    #but they should have the right to change this flag
                    self.mapped('invoice_ids').sudo().write({'invoice_sent': True})
                for inv in self.invoice_ids:
                    if hasattr(inv, 'attachment_ids') and inv.attachment_ids:
                        inv._message_set_main_attachment_id([(False,att) for att in inv.attachment_ids.ids])
        else:
            self._send_email()
        if self.is_print:
            return self._print_document()
        return {'type': 'ir.actions.act_window_close'}

