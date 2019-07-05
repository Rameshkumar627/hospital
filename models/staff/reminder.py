#

from odoo import models, fields
from datetime import datetime

Current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Reminder(models.Model):
    _name = "arc.reminder"

    date = fields.Datetime(string="Date", default=Current_time, required=True)
    employee_id = fields.Many2one(comodel_name="arc.employee", string="Doctor/ Staff", required=True)
    reminder = fields.Text(string="Reminder", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

