import os
import time
import stat
import psycopg2
import datetime
import traceback
import logging
import tempfile
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError, _logger

_logger = logging.getLogger(__name__)


class BIConnector(models.Model):
    _name = "bi.connector"

    _description = 'BI Connector'

    db_host = fields.Char(string='Database Host Name', help='Database hostname on which PostgreSQL is running')  # 'rds_host_url'
    db_user_name = fields.Char(string='Username', help='Username existing in the PostgreSQL database')  # 'your_name'
    db_password = fields.Char(string='Password', help='Password of the database user')  # 'your_db_password'
    db_name = fields.Char(string='Database Name', default='postgres')  # 'your_database_name'
    db_port = fields.Char(string='Database Port', help='Port number required for connecting with database')  # 'port'
    db_name_for_backup = fields.Char(string='Database Instance', help='Database name for data restore')
    logs = fields.Char(string='Last Update', default="Logs:__")

    @api.model
    def checkupdate(self, vals):
        connection = None
        try:
            connection = psycopg2.connect(
                database=vals['database'],
                user=vals['user'],
                password=vals['password'],
                host=vals['host'],
                port=vals['port']
            )
            
            if connection:
                cursor = connection.cursor()
                check_table = '''select count(*) from information_schema.tables where table_schema = 'public';'''
                cursor.execute(check_table)
                list_tables = cursor.fetchall()
                # print(list_tables)
                if (list_tables == [(0,)]):
                    print("database is empty")
                    connection.close()
                    return True
                else:
                    print("database is not empty")
                    connection.close()
                    return False
        except Exception as e:
            print(e)
        finally:
            if connection:
                connection.close()

    @api.model
    def create(self, vals):
        if 'db_name' not in vals:
            vals['db_name'] = 'postgres'
        if 'db_name_for_backup' in vals:
            vals['db_name_for_backup'] = vals['db_name_for_backup'].replace(" ", "")
            obj = self.env['bi.connector'].sudo().search([('db_name_for_backup', '=', vals['db_name_for_backup'])]).ids
            if obj:
                raise ValidationError("Database name is not unique")
        
        print(vals)
        connection = None
        try:
            connection = psycopg2.connect(
                database=vals['db_name'],
                user=vals['db_user_name'],
                password=vals['db_password'],
                host=vals['db_host'],
                port=vals['db_port']
            )

        except Exception as e:
            print(e)
            print("Incorrect credentials Please check and try again: Create")
            raise ValidationError("Incorrect credentials Please check and try again")
        finally:
            if connection:
                connection.close()
        return super(BIConnector, self).create(vals)


    def write(self, vals):
        if 'db_name_for_backup' in vals:
            vals['db_name_for_backup'] = vals['db_name_for_backup'].replace(" ", "")
            obj = self.env['bi.connector'].sudo().search([('db_name_for_backup', '=', vals['db_name_for_backup'])]).ids
            if len(obj) > 0 or (len(obj) == 1 and self.id not in obj):
                raise ValidationError("Database name is not unique")
        print(vals, self)
        obj = self.env['bi.connector'].sudo().search([('id', '=', self.id)])
        # print(obj)
        updated_vals = {
            'db_name': obj.db_name,
            'db_user_name': obj.db_user_name,
            'db_password': obj.db_password,
            'db_host': obj.db_host,
            'db_port': obj.db_port
        }
        for i in vals:
            updated_vals[i] = vals[i]
        connection = None
        try:
            connection = psycopg2.connect(
                database=updated_vals['db_name'],
                user=updated_vals['db_user_name'],
                password=updated_vals['db_password'],
                host=updated_vals['db_host'],
                port=updated_vals['db_port']
            )
        except Exception as e:
            print(e)
            print("Incorrect credentials Please check and try again: Write")
            raise ValidationError("Incorrect credentials Please check and try again")
        finally:
            if connection:
                connection.close()
        return super(BIConnector, self).write(vals)

    # @api.model
    def backup_script(self):
        # print(cr, uid, ids, name, args, context)
        objs = self.env['bi.connector'].sudo().search([])
        print(objs)
        for obj in objs:
            print(obj)
            db_host = obj.db_host
            user_name = obj.db_user_name
            db_name = obj.db_name
            port = obj.db_port
            db_password = obj.db_password
            db_name_for_backup = obj.db_name_for_backup

            val = {
                'database': db_name_for_backup,
                'user': user_name,
                'password': db_password,
                'host': db_host,
                'port': port
            }
            print(val)

            db_to_bak = self.env.cr.dbname
            print(db_to_bak)
            bak_name = '{}-{:%Y-%m-%d_%H-%M-%S}'.format(db_to_bak, datetime.datetime.now())
            with tempfile.TemporaryDirectory() as tmpdir:
                full_bak_path = os.path.join(tmpdir, bak_name)
                _logger.info('Creating local Database Dump')
                _logger.info('Executing command: /usr/bin/pg_dump -w -Fc %s > %s' % (db_to_bak, full_bak_path))
                os.system('/usr/bin/pg_dump -w -Fc %s > %s' % (db_to_bak, full_bak_path))
                try:
                    _logger.info('Restoring The Database to the RDS server')

                    _logger.info('PGPASSWORD=%s dropdb --host %s --port "%s" --username %s --if-exists %s' % (
                        db_password, db_host, port, user_name, db_name_for_backup))
                    
                    os.system('PGPASSWORD=%s dropdb --host %s --port "%s" --username %s --if-exists %s' % (
                        db_password, db_host, port, user_name, db_name_for_backup))
                    

                    _logger.info('PGPASSWORD=%s createdb --host %s --port "%s" --username %s %s' % (
                        db_password, db_host, port, user_name, db_name_for_backup))
                    
                    os.system('PGPASSWORD=%s createdb --host %s --port "%s" --username %s %s' % (
                        db_password, db_host, port, user_name, db_name_for_backup))
                    

                    status = obj.checkupdate(val)
                    if status == True:
                        _logger.info('Restoring The Database to the RDS server')
                        now = str(datetime.datetime.now())
                        obj.logs = now + ' Restoring The Database to the RDS server \n'

                        os.system('/usr/bin/pg_restore -w --host %s --port %s --username %s --dbname %s --verbose %s' % (
                            db_host, port, user_name, db_name_for_backup, full_bak_path))
                        
                        status = obj.checkupdate(val)
                        if status == False:
                            now = str(datetime.datetime.now())
                            obj.logs = now + ' Restore Completed \n'
                            _logger.info('Restore Completed')
                        else:
                            now = str(datetime.datetime.now())
                            obj.logs = now + ' Restore Failed \n'
                            _logger.info('Restore Failed')
                    else:
                        _logger.info(' Database is used somewhere')
                        now = str(datetime.datetime.now())
                        obj.logs = now + ' Restore Failed(Database is used somewhere) \n'
                except:
                    _logger.error("ERROR: Unable to complete the backup/restore process")
                    _logger.error(traceback.format_exc())
