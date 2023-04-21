# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange("purchase_vendor_bill_id", "purchase_id")
    def _onchange_purchase_auto_complete(self):
        """Remove lines with qty=0 if option selected making invoices."""
        res = super()._onchange_purchase_auto_complete()
        self.invoice_line_ids -= self.invoice_line_ids.filtered(
            lambda x: x.quantity == 0.0
        )
        return res

    @api.depends("sdd_paying_mandate_id")
    def _compute_ultimos_digitos_iban(self):
        for record in self:
            if record.sdd_paying_mandate_id is not None and record.sdd_paying_mandate_id.partner_bank_id is not None:
                cuenta = record.sdd_paying_mandate_id.partner_bank_id.acc_number
                salida = ''
                record.last_digits = ''
                if cuenta:
                    longitud = len(cuenta)
                    if longitud > 4:
                        for i in range(0, longitud - 4):
                            salida += '*'
                        salida += cuenta[-4:]
                        record.last_digits = salida

    last_digits = fields.Char(string="Últimos dígitos IBAN Cliente", compute=_compute_ultimos_digitos_iban, store=False)

