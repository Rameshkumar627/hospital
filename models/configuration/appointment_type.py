#

from odoo import models, fields


class AppointmentType(models.Model):
    _name = "appointment.type"

    name = fields.Char(string="Type", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
