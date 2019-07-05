# -*- coding: utf-8 -*-

from odoo import models, fields


class ArcCompany(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    person_id = fields.Many2one(comodel_name="arc.person", string="Person")
    state_id = fields.Many2one(comodel_name="res.country.state", string="State")
    email = fields.Char(string="E-mail")
    address = fields.Text(string="Address")
