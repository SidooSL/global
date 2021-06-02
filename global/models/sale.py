from odoo import models, fields


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


