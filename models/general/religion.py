# -*- coding: utf-8 -*-

from odoo import models, fields


# Religion
class Religion(models.Model):
    _name = "arc.religion"

    name = fields.Char(string="Religion", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    _sql_constraints = [("name", "unique(name)", "Religion must be unique")]
