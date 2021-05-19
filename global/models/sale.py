from odoo import models, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    cod_factusol = fields.Char(required=False)
    publicar_web = fields.Boolean(string="Publicar en web")
