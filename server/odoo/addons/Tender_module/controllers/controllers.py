# -*- coding: utf-8 -*-
from odoo import http

# class RiyanModule(http.Controller):
#     @http.route('/riyan_module/riyan_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/riyan_module/riyan_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('riyan_module.listing', {
#             'root': '/riyan_module/riyan_module',
#             'objects': http.request.env['riyan_module.riyan_module'].search([]),
#         })

#     @http.route('/riyan_module/riyan_module/objects/<model("riyan_module.riyan_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('riyan_module.object', {
#             'object': obj
#         })