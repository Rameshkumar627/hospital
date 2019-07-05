#

from odoo import models, fields


class Location(models.Model):
    _name = "arc.location"

    name = fields.Char(string="Name", required=True)
    location_uid = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    