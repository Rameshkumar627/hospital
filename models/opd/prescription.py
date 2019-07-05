#

from odoo import models, fields, api, modules
from datetime import datetime
import pdfkit
import base64
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition


CONSUMPTION_TYPE = [("before_food", "Before Food"), ("after_food", "After Food")]
current_date = datetime.now().strftime("%Y-%m-%d")


class Prescription(models.Model):
    _name = "arc.prescription"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor", required=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    general_treatment_id = fields.Many2one(comodel_name="general.treatment", string="OPD")
    ipd_treatment_id = fields.Many2one(comodel_name="ipd.treatment", string="IPD")
    prescription_ids = fields.One2many(comodel_name="prescription.detail", inverse_name="prescription_id")
    file_name = fields.Char(string="File Name", default="Prescription.pdf")
    report_pdf = fields.Binary(string="Prescription")
    comment = fields.Text(string="Comment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.multi
    def get_prescription_table(self):
        record_id = self.env["arc.template"].search([("template_uid", "=", "PRESCRIPTION TABLE")])

        data_table = ""

        for rec in self.prescription_ids:
            morning = "Y" if rec.morning else "-"
            noon = "Y" if rec.noon else "-"
            evening = "Y" if rec.evening else "-"
            consumption_type = rec.consumption_type.title().replace("_", " ")
            data_table = """{0}<tr><td>{1}</td>"
                                            <td>{2}</td>
                                            <td>{3}</td>
                                            <td>{4}</td>
                                            <td>{5}</td>
                                            <td>{6}</td></tr>""".format(data_table,
                                                                        rec.product_id.name,
                                                                        morning,
                                                                        noon,
                                                                        evening,
                                                                        consumption_type,
                                                                        rec.quantity)

        data_dict = {"data_table": data_table}
        html_data = record_id.template.format(**data_dict)

        return html_data

    @api.multi
    def trigger_generate_pharmacy_invoice(self):
        detail = []
        tax_id = self.env["product.tax"].search([("rate", "=", 0)])
        for rec in self.prescription_ids:
            detail.append((0, 0, {"product_id": rec.product_id.id,
                                  "tax_id": tax_id.id,
                                  "quantity": rec.quantity}))

        invoice_id = self.env["arc.invoice"].create({"person_id": self.patient_id.person_id.id,
                                                     "invoice_type": "pharmacy",
                                                     "detail_ids": detail})

        return {
            'name': ('Pharmacy Bill'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'arc.invoice',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'res_id': invoice_id.id,
            'context': self.env.context,
        }

    @api.multi
    def trigger_prescription(self):
        record_id = self.env["arc.template"].search([("template_uid", "=", "PRESCRIPTION")])

        data_table = ""

        for rec in self.prescription_ids:
            morning = "Y" if rec.morning else "-"
            noon = "Y" if rec.noon else "-"
            evening = "Y" if rec.evening else "-"
            consumption_type = rec.consumption_type.title().replace("_", " ")
            data_table = """{0}<tr><td>{1}</td>"
                                    <td>{2}</td>
                                    <td>{3}</td>
                                    <td>{4}</td>
                                    <td>{5}</td>
                                    <td>{6}</td></tr>""".format(data_table,
                                                                rec.product_id.name,
                                                                morning,
                                                                noon,
                                                                evening,
                                                                consumption_type,
                                                                rec.quantity)

        data_dict = {"company_logo": "data:image/png;base64,{0}".format(self.company_id.logo),
                     "company_name": self.company_id.name if self.company_id.name else "",
                     "company_address": self.company_id.address if self.company_id.address else "",
                     "patient_name": self.patient_id.person_id.name if self.patient_id.person_id.name else "",
                     "patient_id": self.patient_id.person_id.person_uid if self.patient_id.person_id.person_uid else "",
                     "patient_address": self.patient_id.person_id.address(),
                     "info_no": self.name if self.name else "",
                     "info_date": self.date if self.date else "",
                     "data_table": data_table}

        html_data = record_id.template.format(**data_dict)
        css = "/opt/hospital/static/src/css/template.css"
        pdfkit.from_string(html_data, '/opt/kon/out.pdf', css=css)
        pdf_file = open('/opt/kon/out.pdf', 'rb')
        pdf_data = pdf_file.read()
        pdf_file.close()
        out = base64.b64encode(pdf_data)

        self.write({'report_pdf': out, 'file_name': 'prescription.pdf'})

        return {
            'type': 'ir.actions.act_url',
            'url': '/hospital/prescription?model=arc.prescription&id=%s' % (self.id),
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(Prescription, self).create(vals)


class PrescriptionDetail(models.Model):
    _name = "prescription.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Medicine")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    evening = fields.Boolean(string="Evening")
    consumption_type = fields.Selection(selection=CONSUMPTION_TYPE, string="Consumption")
    quantity = fields.Integer(string="Quantity", default=0)
    prescription_id = fields.Many2one(comodel_name="arc.prescription", string="Prescription")


class PrescriptionPDF(http.Controller):
    _cp_path = '/hospital'

    @http.route('/hospital/prescription', type='http', auth="public")
    def harvest_report_xls_download(self, **data):
        record_id = http.request.env['arc.prescription'].search([('id', '=', data.get('id'))])
        if record_id:
            filecontent = base64.b64decode(record_id.report_pdf)
            filename = record_id.file_name
            if filecontent and filename:
                return request.make_response(filecontent,
                                             headers=[('Content-Type', 'application/pdf'),
                                                      ('Content-Disposition', content_disposition(filename))])
        return request.not_found()
