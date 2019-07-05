# -*- coding: utf-8 -*-

from odoo import models, fields


# Identity
class ArcIdentity(models.Model):
    _name = "arc.identity"

    employee_id = fields.Many2one(comodel_name="arc.employee", string="Employee")
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")
    name = fields.Char(string="Identity", required=True)
    reference = fields.Char(string="Identity No", required=True)
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    _sql_constraints = [("name", "unique(name)", "Identity must be unique")]
