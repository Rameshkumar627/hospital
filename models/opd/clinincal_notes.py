#

from odoo import models, fields
from datetime import datetime

Current_date = datetime.now().strftime("%Y-%m-%d")


class ClinicalNotes(models.Model):
    _name = "clinical.notes"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=Current_date, required=True)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor", required=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    notes = fields.Html(string="Notes")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

