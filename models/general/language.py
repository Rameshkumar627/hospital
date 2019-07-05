# -*- coding: utf-8 -*-

from odoo import models, fields


# Language
class Language(models.Model):
    _name = "arc.language"

    name = fields.Char(string="Language", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    _sql_constraints = [("name", "unique(name)", "Language must be unique")]
