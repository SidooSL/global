# -*- coding: utf-8 -*-
# from odoo import http


# class Global(http.Controller):
#     @http.route('/global/global/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/global/global/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('global.listing', {
#             'root': '/global/global',
#             'objects': http.request.env['global.global'].search([]),
#         })

#     @http.route('/global/global/objects/<model("global.global"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('global.object', {
#             'object': obj
#         })
