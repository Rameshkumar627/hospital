# -*- coding: utf-8 -*-

from odoo import models, fields


class DischargeReason(models.Model):
    _name = "discharge.reason"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

