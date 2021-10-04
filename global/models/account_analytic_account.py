# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo import api, models, fields, _
class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    correo_electronico = fields.Char("Correo electrónico")