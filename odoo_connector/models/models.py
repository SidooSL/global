# -*- coding: utf-8 -*-
from odoo import models, fields, api
import os, base64, requests

import logging
from odoo.exceptions import _logger

_logger = logging.getLogger(__name__)


class odoo_connector(models.Model):
    _name = 'odoo.connector'
    _description = 'odoo.connector'
    _rec_name = 'db_name'

    attachment_file = fields.Binary(string="Backup File")
    store_fname = fields.Char(string="File Name")

    api_base_url = fields.Char(string='API Base URL')

    db_host = fields.Char(string='Database Host Name')
    db_username = fields.Char(string='Database Username')
    db_password = fields.Char(string='Database Password')
    db_port = fields.Char(string='Database Port')
    db_name = fields.Char(string='Database Name')

    logs = fields.Text(string='Logs', default="")

    def daily_script(self, *args, **kwargs):

        _logger.info('----------------Daily process is started, please wait for a few seconds.----------------')

        connector_object = self.env['odoo.connector'].sudo().search([])[0]
        connector_object.logs = "Daily process is started, please wait for a few seconds."
        full_api_base_url = f'http://{connector_object.api_base_url}/upload-data'

        path_daily_backup = os.path.join(os.getcwd(), "backup.daily")
        daily_backup_folder = os.listdir(path_daily_backup)

        backup_file = [string for string in daily_backup_folder if "daily.sql.gz" in string]

        try:
            if backup_file:
                backup_file_path = os.path.join(path_daily_backup, backup_file[0])

                _logger.info(
                    backup_file_path + '----------------Daily process is started, please wait for a few seconds.----------------')

                with open(backup_file_path, 'rb') as _file:
                    connector_object.store_fname = backup_file[0]
                    connector_object.write({"attachment_file": base64.b64encode(_file.read())})

                _logger.info(
                    connector_object.store_fname + '----------------Daily process is started, please wait for a few seconds.----------------')

                requests.get(full_api_base_url)
            else:
                print("Not Found: No daily backup found.")

        except Exception as e:
            print('Error', e)

    def manual_script(self, *args, **kwargs):
        self.logs = "Manual process is started, please wait for a few seconds."

        path_daily_backup = os.path.join(os.getcwd(), "backup.daily")
        daily_backup_folder = os.listdir(path_daily_backup)

        manual_files = [string for string in daily_backup_folder if "manual.sql.gz" in string]
        full_api_base_url = f'http://{self.api_base_url}/upload-data'

        try:
            if manual_files:
                manual_backup_file = sorted(manual_files)[-1]
                backup_file_path = os.path.join(path_daily_backup, manual_backup_file)

                with open(backup_file_path, 'rb') as _file:
                    self.store_fname = manual_backup_file
                    self.write({"attachment_file": base64.b64encode(_file.read())})

                requests.get(full_api_base_url)
            else:
                print("Not Found: No daily backup found.")

        except Exception as e:
            print('Error', e)


