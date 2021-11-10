# -*- coding: utf-8 -*-

from . import controllers
from . import models

from odoo import api, SUPERUSER_ID

import logging
_logger = logging.getLogger(__name__)

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.config_parameter'].search([('key', 'like', 'powerbi_script')]).unlink()