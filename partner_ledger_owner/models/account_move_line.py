from odoo import fields, models, api


class accountMoveline(models.Model):
    _inherit = "account.move.line"
    owner_name = fields.Char('Owner Name',required=False)
    village_name = fields.Char('Village Name', required=False)
    @api.model
    def create(self,vals):
        res = super(accountMoveline,self).create(vals)
        res.owner_name = res.partner_id.owner_name if res.partner_id else ''
        res.village_name = res.partner_id.village_name if res.partner_id else ''
        return res




