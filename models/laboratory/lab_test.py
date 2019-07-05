# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pdfkit
import base64

PROGRESS_INFO = [("draft", "Draft"), ("completed", "Completed")]


class LabTest(models.Model):
    _name = "lab.test"

    name = fields.Char(string="Name", readonly=True)
    master_id = fields.Many2one(comodel_name="lab.master", string="Lab-Test")
    price = fields.Float(string="Price")
    template = fields.Html(string="Template")
    report = fields.Html(string="Report")
    value_ids = fields.One2many(comodel_name="lab.test.detail.value", inverse_name="lab_id")
    image_ids = fields.One2many(comodel_name="lab.test.detail.image", inverse_name="lab_id")
    laboratory_id = fields.Many2one(comodel_name="arc.lab", string="Laboratory")
    report_pdf = fields.Binary(string="Report")
    file_name = fields.Char(string="File Name", default="report.pdf")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    comment = fields.Text(string="Comment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.multi
    def trigger_report(self):
        value_recs = self.value_ids
        image_recs = self.image_ids

        data = {}
        for rec in value_recs:
            if rec.value:
                data[rec.sequence] = rec.value
            else:
                data[rec.sequence] = ""

        for rec in image_recs:
            if rec.image:
                data[rec.sequence] = rec.image
            else:
                data[rec.sequence] = ""

        data[0] = self.laboratory_id.name
        data[1] = self.laboratory_id.patient_id.name
        data[2] = self.laboratory_id.patient_id.patient_uid
        data[3] = self.laboratory_id.patient_id.address
        data[4] = self.laboratory_id.patient_id.mobile
        data[5] = self.laboratory_id.patient_id.email

        print data

        template = self.template

        if self.paramsi == 13:
            report = template.format(data[0],
                                     data[1],
                                     data[2],
                                     data[3],
                                     data[4],
                                     data[5],
                                     data[6],
                                     data[7],
                                     data[8],
                                     data[9],
                                     data[10],
                                     data[11],
                                     data[12],
                                     data[13])
        if self.paramsi == 9:
            report = template.format(data[0],
                                     data[1],
                                     data[2],
                                     data[3],
                                     data[4],
                                     data[5],
                                     data[6],
                                     data[7],
                                     data[8])

        if self.paramsi == 7:
            report = template.format(data[0],
                                     data[1],
                                     data[2],
                                     data[3],
                                     data[4],
                                     data[5],
                                     data[6],
                                     data[7])

        self.report = report
        pdfkit.from_string(report, '/opt/kon/out.pdf')

        pdf_file = open('/opt/kon/out.pdf', 'rb')
        out = pdf_file.read()
        pdf_file.close()
        gentextfile = base64.b64encode(out)

        self.report_pdf = gentextfile
        self.progress = "completed"

    @api.model
    def create(self, vals):
        master_rec = self.env["lab.master"].search([("id", "=", vals["master_id"])])
        value_recs = self.env["lab.master.detail.value"].search([("lab_id", "=", vals["master_id"])])
        image_recs = self.env["lab.master.detail.image"].search([("lab_id", "=", vals["master_id"])])

        vals["price"] = master_rec.price
        vals["template"] = master_rec.template
        vals["paramsi"] = master_rec.paramsi
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        lab_id = super(LabTest, self).create(vals)

        for rec in value_recs:
            self.env["lab.test.detail.value"].create({"sequence": rec.sequence,
                                                      "name": rec.name,
                                                      "lab_id": lab_id.id})

        for rec in image_recs:
            self.env["lab.test.detail.image"].create({"sequence": rec.sequence,
                                                      "name": rec.name,
                                                      "lab_id": lab_id.id})

        return lab_id


class LabTestDetailValue(models.Model):
    _name = "lab.test.detail.value"

    name = fields.Char(string="Name")
    value = fields.Char(string="Value")
    lab_id = fields.Many2one(comodel_name="lab.test", string="Lab")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)


class LabTestDetailImage(models.Model):
    _name = "lab.test.detail.image"

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    lab_id = fields.Many2one(comodel_name="lab.test", string="Lab")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

