from odoo import models, fields
from odoo.exceptions import UserError
from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        domain="['|', ('id', '=', partner_id), ('parent_id', '=', partner_id),  '|', ('company_id', '=', False), ('company_id', '=', company_id)]", )
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        domain="['|', ('id', '=', partner_id), ('parent_id', '=', partner_id),  '|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    # def action_quotation_sent(self):
    #     """
    #     Se modifica la función para evitar que se autosubscriban los partners
    #     """
    #
    #     if self.filtered(lambda so: so.state != 'draft'):
    #         raise UserError(_('Only draft orders can be marked as sent directly.'))
    #     # TK: Hemos eliminado esto
    #     # for order in self:
    #     #     order.message_subscribe(partner_ids=order.partner_id.ids)
    #     self.write({'state': 'sent'})
    #
    # def action_confirm(self):
    #     """
    #     Se modifica la función para evitar que se autosubscriban los partners
    #     """
    #     if self._get_forbidden_state_confirm() & set(self.mapped('state')):
    #         raise UserError(_(
    #             'It is not allowed to confirm an order in the following states: %s'
    #         ) % (', '.join(self._get_forbidden_state_confirm())))
    #
    #     # TK: Hemos eliminado esto
    #     # for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
    #     #     order.message_subscribe([order.partner_id.id])
    #
    #     self.write({
    #         'state': 'sale',
    #         'date_order': fields.Datetime.now()
    #     })
    #
    #     # Context key 'default_name' is sometimes propagated up to here.
    #     # We don't need it and it creates issues in the creation of linked records.
    #     context = self._context.copy()
    #     context.pop('default_name', None)
    #
    #     self.with_context(context)._action_confirm()
    #     if self.env.user.has_group('sale.group_auto_done_setting'):
    #         self.action_done()
    #     return True
