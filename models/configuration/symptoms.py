#

from odoo import models, fields


class Symptoms(models.Model):
    _name = "arc.symptoms"

    name = fields.Char(string="Symptoms", required=True)
    symptoms_uid = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

