from odoo import models, fields, api,_
from num2words import num2words

class AccountBankStatementLine (models.Model):
    _inherit = 'account.bank.statement.line'

    total_in_words = fields.Char(compute="_total_in_words")

    @api.depends('amount')
    def _total_in_words(self):
        for rec in self:
            if rec.amount:
                rec.total_in_words = num2words(rec.amount, lang='ar')
