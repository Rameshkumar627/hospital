#

from odoo import models, fields, api

DAY = [("monday", "Monday"),
       ("tuesday", "Tuesday"),
       ("wednesday", "Wednesday"),
       ("thursday", "Thursday"),
       ("friday", "Friday"),
       ("saturday", "Saturday"),
       ("sunday", "Sunday")]


class DoctorTimings(models.Model):
    _name = "doctor.timings"

    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor", required=True)
    timings_ids = fields.One2many(comodel_name="timings.detail", inverse_name="timing_id")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        timings_id = super(DoctorTimings, self).create(vals)

        for rec in DAY:
            self.env["timings.detail"].create({"day": rec[0], "timing_id": timings_id.id})

        return timings_id


class TimingsDetail(models.Model):
    _name = "timings.detail"

    day = fields.Selection(selection=DAY, string="Day")
    from_morning = fields.Float(string="From Morning")
    till_morning = fields.Float(string="Till Morning")
    from_evening = fields.Float(string="From Evening")
    till_evening = fields.Float(string="Till Evening")
    timing_id = fields.Many2one(comodel_name="doctor.timings", string="Timings")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
