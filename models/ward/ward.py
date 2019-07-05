# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Ward(models.Model):
    _name = "arc.ward"

    name = fields.Char(string="Name", required=True)
    ward_uid = fields.Char(string="Code", required=True)
    bed_ids = fields.One2many(comodel_name="arc.bed", inverse_name="ward_id", string="Bed")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

