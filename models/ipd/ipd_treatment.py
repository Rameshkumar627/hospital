# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import pdfkit
import base64

current_date = datetime.now().strftime("%Y-%m-%d")


class IPDTreatment(models.Model):
    _name = "ipd.treatment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    image = fields.Binary(string="Image")
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor", required=True)
    bed_id = fields.Many2one(comodel_name="arc.bed", string="Bed", required=True)
    diagnosis_ids = fields.Many2many(comodel_name="arc.diagnosis", string="Diagnosis")
    diagnosis_comment = fields.Text(string="Comment")
    treatment_detail = fields.One2many(comodel_name="ipd.treatment.detail", inverse_name="ipd_id")
    prescription_ids = fields.One2many(comodel_name="arc.prescription", inverse_name="ipd_treatment_id")
    report = fields.Html(string="Report")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    file_name = fields.Char(string="File Name", default="treatment.pdf")
    report_pdf = fields.Binary(string="Report")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(IPDTreatment, self).create(vals)


class IPDTreatmentDetail(models.Model):
    _name = "ipd.treatment.detail"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    diagnosis_ids = fields.Many2many(comodel_name="arc.diagnosis", string="Diagnosis")
    treatment_ids = fields.Many2many(comodel_name="arc.treatment", string="Treatment")
    comment = fields.Text(string="Comment")
    ipd_id = fields.Many2one(comodel_name="ipd.treatment", string="Treatment", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(IPDTreatmentDetail, self).create(vals)
