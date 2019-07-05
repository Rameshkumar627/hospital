#

from odoo import models, fields


class InvoiceDescription(models.Model):
    _name = "invoice.description"

    name = fields.Char(string="Description", required=True)
    code = fields.Char(string="Code")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

