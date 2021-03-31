from odoo import models, fields


class ResPartner(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    marca = fields.Char(required=False, string="Marca")