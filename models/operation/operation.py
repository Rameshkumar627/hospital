# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


# Operation
class Operation(models.Model):
    _name = "arc.operation"

    name = fields.Char(string="Name", required=True)
    operation_uid = fields.Char(string="Code", required=True)
    procedure = fields.Html(string="Operation Procedure")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    comment = fields.Text(string="Comment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

