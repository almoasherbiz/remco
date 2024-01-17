
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    # journal_id = fields.Many2one(
    #     comodel_name='account.journal',readonly=False,
    #     domain="[('type', 'in', ('bank', 'cash'))]")

    journal_id = fields.Many2one(
        comodel_name='account.journal',
        compute='_compute_available_journal_ids', store=True, readonly=False, precompute=True,
        domain="[('id', 'in', available_journal_ids)]")

    @api.depends('payment_type', 'company_id', 'can_edit_wizard')
    def _compute_available_journal_ids(self):
        for wizard in self:
            wizard.available_journal_ids = self.env['account.journal'].search([
                ('company_id', '=', wizard.company_id.id),
                ('type', 'in', ('bank', 'cash')),
            ])
class ACCOUNTMOVE(models.Model):
    _inherit = 'account.move'

    owner_name = fields.Char('Owner Name',related="partner_id.owner_name")
    village_name = fields.Char('Village Name',related="partner_id.village_name")
class Partner(models.Model):
    _inherit = 'res.partner'
    is_customer = fields.Boolean()
    customer_credit_check = fields.Boolean(compute="change_owner")

    owner_name = fields.Char('Owner Name', )
    village_name = fields.Char('Village Name',)
    partner_ledger_limit = fields.Integer("Partner Ledger Limit")

    # @api.constrains("owner_name")
    @api.depends("total_due")
    def change_owner(self):
        for rec in self:
            rec.customer_credit_check=False
            if rec.total_due <= 0:
                rec.customer_credit_check = True


    # @api.constrains("owner_name")
    # @api.onchange("owner_name")
    # def _change_owner(self):
    #     for rec in self:
    #         print('fffffffff',rec.total_due)
    #         if rec.partner_ledger_limit < rec.total_due:
    #            # self.env.cr.rollback()
    #            raise ValidationError(_('You cannot change Owner Name!'))

