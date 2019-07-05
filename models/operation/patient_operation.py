# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"),
                 ("ot_booked", "OT Booked"),
                 ("done", "Done"),
                 ("cancel", "Cancel")]
current_date = datetime.now().strftime("%Y-%m-%d")


# Patient Operation
class PatientOperation(models.Model):
    _name = "patient.operation"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor", required=True)
    staff_ids = fields.Many2many(comodel_name="arc.employee", string="Staffs")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    # Operation
    operation_date = fields.Date(string="Date of Operation", default=current_date, required=True)
    operation_id = fields.Many2one(comodel_name="arc.operation", string="Operation", required=True)
    procedure = fields.Binary(string="Procedure")
    ot_id = fields.Many2one(comodel_name="operation.theater", string="Operation Theater", required=True)
    comment = fields.Text(string="Comment")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    @api.multi
    def trigger_ot_booked(self):
        self.write({"progress": "ot_booked"})

    @api.multi
    def trigger_done(self):
        self.write({"progress": "done"})

    @api.multi
    def trigger_cancel(self):
        self.write({"progress": "cancel"})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(PatientOperation, self).create(vals)
