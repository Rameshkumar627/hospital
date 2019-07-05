#

from odoo import models, fields
from datetime import datetime

Current_date = datetime.now().strftime("%Y-%m-%d")


class Notes(models.Model):
    _name = "arc.notes"

    date = fields.Date(string="Date", default=Current_date, required=True)
    employee_id = fields.Many2one(comodel_name="arc.employee", string="Doctor/ Staff", required=True)
    notes = fields.Text(string="Notes")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

