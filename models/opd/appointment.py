# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

APPOINTMENT_TYPE = [("opt", "OPT"), ("meeting", "Meeting"), ("others", "Others")]
PROGRESS_INFO = [("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Appointment
class Appointment(models.Model):
    _name = "arc.appointment"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    name = fields.Char(string="Name", readonly=True)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Person", required=True)
    appointment_type = fields.Selection(selection=APPOINTMENT_TYPE, default="opt", required=True)
    appointment_for = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    reason = fields.Many2one(comodel_name="appointment.reason", string="Reason", required=True)
    comment = fields.Text(string="Comment")
    is_cancel = fields.Selection(selection=PROGRESS_INFO, string="Is Cancel")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        sequence = "{0}.{1}".format(self._name, vals["appointment_type"])
        vals["name"] = self.env["ir.sequence"].next_by_code(sequence)
        return super(Appointment, self).create(vals)

    @api.multi
    def trigger_cancel(self):
        self.write({"is_cancel": "cancel"})
