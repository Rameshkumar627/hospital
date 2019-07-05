# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


# Operation Theater
class OperationTheater(models.Model):
    _name = "operation.theater"

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Image")
    theater_uid = fields.Char(string="Code", required=True)
    operation_ids = fields.One2many(comodel_name="patient.operation", inverse_name="ot_id")
    supervisor_id = fields.Many2one(comodel_name="arc.person", string="In-Charge")
    theater_facility = fields.Html(string="Theater Facility")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

