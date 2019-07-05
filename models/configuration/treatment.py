#

from odoo import models, fields


class Treatment(models.Model):
    _name = "arc.treatment"

    name = fields.Char(string="Treatment", required=True)
    treatment_uid = fields.Char(string="Code", required=True)
    description = fields.Html(string="Description")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

