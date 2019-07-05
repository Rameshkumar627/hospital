#

from odoo import models, fields


class Fee(models.Model):
    _name = "arc.fee"

    name = fields.Char(string="Fees", required=True)
    fee_uid = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

