# -*- coding: utf-8 -*-
# from odoo import http


# class PartnerUnitTab(http.Controller):
#     @http.route('/partner_unit_tab/partner_unit_tab', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_unit_tab/partner_unit_tab/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_unit_tab.listing', {
#             'root': '/partner_unit_tab/partner_unit_tab',
#             'objects': http.request.env['partner_unit_tab.partner_unit_tab'].search([]),
#         })

#     @http.route('/partner_unit_tab/partner_unit_tab/objects/<model("partner_unit_tab.partner_unit_tab"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_unit_tab.object', {
#             'object': obj
#         })
