#

from odoo import models, fields


class Diagnosis(models.Model):
    _name = "arc.diagnosis"

    name = fields.Char(string="Diagnosis", required=True)
    diagnosis_uid = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
