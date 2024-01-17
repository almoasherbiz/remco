# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    counter_paid = fields.Boolean()
    payment_date = fields.Date()
    receipt_number = fields.Char()

    unit_space = fields.Float()
    garden_space = fields.Float()
    roof_space = fields.Float()

    unit_receipt_date = fields.Date()
    deposit_payment_date = fields.Date()
    deposit_amount = fields.Float()

    notes_1 = fields.Text()
    notes_2 = fields.Text()
    notes_3 = fields.Text()
