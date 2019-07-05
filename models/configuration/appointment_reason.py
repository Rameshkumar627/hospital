#

from odoo import models, fields


class AppointmentReason(models.Model):
    _name = "appointment.reason"

    name = fields.Char(string="Reason", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
