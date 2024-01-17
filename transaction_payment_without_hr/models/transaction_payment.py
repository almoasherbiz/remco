from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from random import choice
from string import digits



# default_account_id


from datetime import datetime


class AccountPaymentsss(models.Model):

    _inherit = 'account.payment'
    transaction_payment= fields.Boolean(default=False)

class AccounTransaction(models.Model):
    _name='payment.transaction.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name=fields.Char()
    destination_account_id = fields.Many2one('account.account', required=1)
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, readonly=False,
                                  compute='_compute_currency_id',
                                  help="The payment's currency.")
    amount = fields.Monetary(currency_field='currency_id')
    payment_type = fields.Selection([
        ('outbound', 'Send'),
        ('inbound', 'Receive'),
    ], string='Payment Type', default='outbound', required=True, tracking=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
        store=True, readonly=False, ondelete='restrict',
        compute='_compute_partner_id',
        domain="['|', ('parent_id','=', False), ('is_company','=', True)]",
        tracking=True,
        check_company=True)
    date=fields.Date(default=datetime.today())
    ref =fields.Char()
    label =fields.Char(required=1)

    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        domain="[('type', 'in', ('bank','cash')), ('company_id', '=', company_id)]",
        check_company=True,
    )

    product_id=fields.Many2one('product.product',string="Activity Type")
    company_id  = fields.Many2one("res.company",default=lambda self:self.env.company.id)

    # partner_bank_id = fields.Many2one('res.partner.bank', string="Recipient Bank Account",
    #                                   readonly=False, store=True, tracking=True,
    #                                   compute='_compute_partner_bank_id',
    #                                   domain="[('id', 'in', available_partner_bank_ids)]",
    #                                   check_company=True)
    #
    # available_partner_bank_ids = fields.Many2many(
    #     comodel_name='res.partner.bank',
    #     compute='_compute_available_partner_bank_ids',
    # )

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')

    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Journal Entry', readonly=True, ondelete='cascade',
        check_company=True, )

    # commision_prsg = fields.Float(digits=(12, 1))
    # employee = fields.Char(string='Sales Employee')
    user_id = fields.Many2one('res.users', string='Created By',default=lambda self:self.env.user.id)
    analytic_account_h = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_h = fields.Many2one('account.analytic.tag', string='Analytic Tags')
    # reconciled_statements_count = fields.Integer(string="# Reconciled Statements",
    #                                              compute="_compute_stat_buttons_from_reconciliation")



    @api.depends('journal_id')
    def _compute_currency_id(self):
        for pay in self:
            pay.currency_id = pay.journal_id.currency_id or pay.journal_id.company_id.currency_id

    # @api.model
    # def create(self, vals):
    #     result = super(AccounTransaction, self).create(vals)
    #     result.name = self.env['ir.sequence'].next_by_code('payment.transaction.model') or 'New'
    #     return result




    def button_open_journal_entry(self):
        ''' Redirect the user to this payment journal.
        :return:    An action on account.move.
        '''
        self.ensure_one()
        return {
            'name': _("Journal Entry"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'context': {'create': False},
            'view_mode': 'form',
            'res_id': self.move_id.id,
        }

    # @api.depends('partner_id', 'payment_type', 'journal_id')
    # def _compute_available_partner_bank_ids(self):
    #     for pay in self:
    #         if pay.payment_type == 'inbound':
    #             pay.available_partner_bank_ids = pay.journal_id.bank_account_id
    #
    #         else:
    #             pay.available_partner_bank_ids = pay.partner_id.bank_ids \
    #                 .filtered(lambda x: x.company_id.id in (False, pay.company_id.id))._origin







    destination_account=fields.Many2one('account.account')

    def action_draft(self):
        self.state='draft'
        move_id=self.env['account.move'].search([('state','!=','cancel'),('id','=',self.move_id.id)])
        for move in move_id:
            move.button_cancel()

    def post_transaction(self):

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for item in self:
            ratio=1
            if item.currency_id.id != self.company_id.currency_id:
                ratio = self.currency_id.rate

            if item.payment_type=='inbound':


                if item.partner_id:
                    partner = self.partner_id.id
                else:
                    partner = False

                if item.analytic_tag_h:
                    analytic_tag = not bool([item.analytic_tag_h.id])
                else:
                    analytic_tag = False

                move_vals = {

                    'journal_id': item.journal_id.id,
                    # 'commision_prsg': item.commision_prsg,
                    # 'employee_id': item.employee_id.id,
                    'ref':item.ref,

                    'date': item.date,
                    'line_ids': [
                        (0, 0, {

                            'debit': item.amount /ratio,
                            'name': item.label,
                            'credit': 0,
                            'account_id': item.journal_id.default_account_id.id,
                            'analytic_account_id': item.analytic_account_h.id,
                            'analytic_tag_ids': analytic_tag,
                            'product_id': item.product_id.id,
                            'partner_id': partner,
                            'currency_id': item.currency_id.id if item.currency_id != item.company_id.currency_id else '',
                            'amount_currency': item.amount if ratio != 1 else 0,
                        }
                         ),
                        (0, 0, {

                            'debit': 0,
                            'name': item.label,
                            'credit': item.amount/ratio,
                            'account_id': item.destination_account_id.id,
                            'analytic_account_id': item.analytic_account_h.id,
                            'analytic_tag_ids': analytic_tag,
                            'product_id': item.product_id.id,
                            'partner_id': partner,
                            'currency_id': item.currency_id.id if item.currency_id != item.company_id.currency_id else '',
                            'amount_currency': -item.amount if ratio != 1 else 0,
                        }),

                    ]}
            else:

                if item.partner_id:
                    partner = item.partner_id.id
                else:
                    partner = False

                if item.analytic_tag_h:
                    analytic_tag = not bool([item.analytic_tag_h.id])
                else:
                    analytic_tag = False
                move_vals = {

                    'journal_id': item.journal_id.id,
                    'ref': item.ref,
                    'date': item.date,
                    # 'employee_id':item.employee_id.id,
                    # 'commision_prsg': item.commision_prsg,
                    'line_ids': [
                        (0, 0, {
                            'name': item.label,
                            'debit': item.amount/ratio,
                            'credit': 0,
                            'account_id':  item.destination_account_id.id,
                            'analytic_account_id': item.analytic_account_h.id,
                            'analytic_tag_ids': analytic_tag,
                            'product_id': item.product_id.id,
                            'partner_id': partner,
                            'currency_id': item.currency_id.id if item.currency_id != item.company_id.currency_id else '',
                            'amount_currency': item.amount if ratio != 1 else 0,
                        }
                         ),
                        (0, 0, {
                            'name': item.label,
                            'debit': 0,
                            'credit': item.amount/ratio,
                            'account_id':item.journal_id.default_account_id.id,
                            'analytic_account_id': item.analytic_account_h.id,
                            'analytic_tag_ids':analytic_tag,
                            'product_id': item.product_id.id,
                            'partner_id': partner,
                            'currency_id': item.currency_id.id if item.currency_id != item.company_id.currency_id else '',
                            'amount_currency': -item.amount if ratio != 1 else 0,
                        }
                         ),

                    ]}
        move = self.env['account.move'].create(move_vals)
        move.action_post()
        self.name=move.name
        #
        self.move_id=move.id
        self.state='posted'




