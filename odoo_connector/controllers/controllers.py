import werkzeug
import base64
import json
from odoo import http
from odoo.http import request, route, Controller, Response

key = "decdeco"
# key = "JHI1KIlbvUMu0B7ivTUMcLXWc"
# token = "DbRYiaJLayP7sQa"
token = "passpass"


# enc = 5DFMZC>@R[D+d3U


class OdooConnector(Controller):

    def decrypt(self, key, encryped_token):
        decrypted_token = []
        for i, c in enumerate(encryped_token):
            key_c = ord(key[i % len(key)])
            enc_c = ord(c)
            decrypted_token.append(chr((enc_c - key_c) % 127))
        return ''.join(decrypted_token)

    @route('/bi-connector/dump-download', type='http', auth="public")
    def download_document(self, **kw):
        file_name = 'dump.sql.gz'
        encryped_token = kw.get('token')
        print(encryped_token)
        decryped_token = self.decrypt(key, encryped_token)

        if decryped_token == token:
            print("pass")
            Model = request.env['odoo.connector'].sudo().search([('id', '=', 1)])
            filecontent = base64.b64decode(Model.attachment_file or '')
            headers = werkzeug.datastructures.Headers()

            if not filecontent:
                return request.not_found()
            else:
                if not file_name:
                    filename = '%s_%s' % (Model.replace('.', '_'), id)
                    headers.add('Content-Disposition', 'attachment', filename=filename)
                    return request.make_response(filecontent, headers)
                else:
                    headers.add('Content-Disposition', 'attachment', filename=file_name)
                    return request.make_response(filecontent, headers)
        else:
            print("token mismatch")
            return request.not_found()

    @route(['/bi-connector/connection-details'], type='http', csrf=False, auth='public', methods=['GET'], website=True)
    def connection_details(self, **kwargs):

        connector_object = request.env['odoo.connector'].sudo().search([])

        data = {
            'db_host': connector_object.db_host,
            'db_username': connector_object.db_username,
            'db_password': connector_object.db_password,
            'db_port': connector_object.db_port,
            'db_name': connector_object.db_name,
        }

        return Response(
            json.dumps({'data': data}),
            content_type='application/json;charset=utf-8',
            status=200
        )

    @route(['/bi-connector/logs'], type='http', csrf=False, auth='public', methods=['POST'], website=True)
    def logs(self, **kwargs):

        logs = kwargs.get('logs')

        connector_object = request.env['odoo.connector'].sudo().search([])
        connector_object.write({'logs': logs})

        return Response(
            json.dumps({'logs': logs}),
            content_type='application/json;charset=utf-8',
            status=200
        )
