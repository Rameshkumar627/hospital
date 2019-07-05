# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("shifted", "Shifted")]
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class PatientShifting(models.Model):
    _name = "patient.shifting"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", default=current_time, required=True)
    name = fields.Char(string="Name", readonly=True)
    treatment_id = fields.Many2one(comodel_name="ipd.treatment", string="Patient")
    source_id = fields.Many2one(comodel_name="arc.bed", string="Source")
    destination_id = fields.Many2one(comodel_name="arc.bed", string="Destination")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    comment = fields.Text(string="Comment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.multi
    def trigger_shifting(self):
        self.write({"progress": "shifted"})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(PatientShifting, self).create(vals)
