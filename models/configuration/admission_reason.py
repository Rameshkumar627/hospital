# -*- coding: utf-8 -*-

from odoo import models, fields


class AdmissionReason(models.Model):
    _name = "admission.reason"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
