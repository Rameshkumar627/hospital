#

from odoo import models, fields, api
from datetime import datetime
import pdfkit
import base64

current_date = datetime.now().strftime("%Y-%m-%d")


class DentalTreatment(models.Model):
    _name = "dental.treatment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor", required=True)
    symptoms_ids = fields.Many2many(comodel_name="arc.symptoms", string="Symptoms")
    diagnosis_ids = fields.Many2many(comodel_name="arc.diagnosis", string="Diagnosis")
    diagnosis_comment = fields.Text(string="Comment")
    treatment_ids = fields.Many2many(comodel_name="arc.treatment", string="Treatment")
    treatment_comment = fields.Text(string="Comment")
    prescription_ids = fields.One2many(comodel_name="arc.prescription", inverse_name="general_treatment_id", string="Prescription")
    report = fields.Html(string="Report")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    file_name = fields.Char(string="File Name", default="treatment.pdf")
    report_pdf = fields.Binary(string="Report")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    def get_comma(self, recs):
        record = ""
        for rec in recs:
            if record == "":
                record = "{1}({2})".format(record, rec.name, rec.code)
            else:
                record = "{0}, {1}({2})".format(record, rec.name, rec.code)

        return record

    @api.multi
    def generate_report(self):
        symptoms = self.get_comma(self.symptoms_ids)
        diagnosis = self.get_comma(self.diagnosis_ids)
        treatment = self.get_comma(self.treatment_ids)
        diagnosis_comment = self.diagnosis_comment or ""
        treatment_comment = self.treatment_comment or ""

        header = """<table>
                        <tr><td>{0}</td></tr>
                        <tr><td>{1}</td></tr>
                        <tr><td>{2}</td></tr>
                        <tr><td>{3}</td></tr>
                    </table>""".format(self.date, self.name, self.doctor_id.name, self.patient_id.name)

        body = """<table>
                        <tr><td style="width: 100px;">Symptoms</td><td>{0}</td></tr>
                        <tr><td>Diagnosis</td><td>{1}</td></tr>
                        <tr><td></td><td>{2}</td></tr>
                        <tr><td>Treatment</td><td>{3}</td></tr>
                        <tr><td></td><td>{4}</td></tr>
                  </table>""".format(symptoms, diagnosis, diagnosis_comment, treatment, treatment_comment)

        treatment_detail = self.get_dental_table()

        prescription = self.prescription_id.get_dental_table()

        html = self.prescription_id.get_static_file()

        report = "{0}{1}{2}{3}".format(header, body, treatment_detail, prescription)
        new_report = html.format(report)

        self.report = new_report

        pdfkit.from_string(new_report, '/opt/kon/out.pdf')

        pdf_file = open('/opt/kon/out.pdf', 'rb')
        out = pdf_file.read()
        pdf_file.close()
        gentextfile = base64.b64encode(out)

        self.report_pdf = gentextfile

    @api.multi
    def trigger_register_payment(self):

        return {
            'name': ('Register Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'arc.payment',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_person_id': self.patient_id.person_id.id,
                        'default_ref': self.name}
        }
