from odoo import models, fields, api

class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    def copy_to_other_variants(self):
        self.ensure_one()
        product = self.product_id
        product_done_ids = product.mapped('product_tmpl_id.product_variant_ids.orderpoint_ids.product_id').ids

        products_todo = self.env['product.product'].search([
            ('product_tmpl_id', '=', product.product_tmpl_id.id),
            ('id', 'not in', product_done_ids)
        ])

        for product in products_todo:
            self.copy({
                'product_id': product.id
            })
