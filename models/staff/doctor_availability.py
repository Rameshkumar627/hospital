#

from odoo import models, fields
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")


class DoctorAvailability(models.Model):
    _name = "doctor.availability"

    from_date = fields.Date(string="From Date", default=current_date, required=True)
    till_date = fields.Date(string="Till Date", default=current_date, required=True)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)


