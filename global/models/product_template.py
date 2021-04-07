from odoo import models, fields


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    marca = fields.Char(required=False, string="Marca")
    website_long_description = fields.Html(required=False, string="Descripción larga")