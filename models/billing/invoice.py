# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import base64
import pdfkit
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition


current_date = datetime.now().strftime("%Y-%m-%d")
PROGRESS = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved")]
PAYMENT_PROGRESS = [("un_paid", "Un-Paid"), ("partially_paid", "Partially Paid"), ("paid", "Paid")]
INVOICE_TYPE = [("pharmacy", "Pharmacy"), ("purchase", "Purchase"), ("treatment", "Treatment")]


class Invoice(models.Model):
    _name = "arc.invoice"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Person", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    progress = fields.Selection(selection=PROGRESS, string="Progress", default="draft")
    payment_progress = fields.Selection(selection=PAYMENT_PROGRESS, string="Payment Progress", compute="_get_payment_progress")
    invoice_type = fields.Selection(selection=INVOICE_TYPE, string="Invoice Type")
    detail_ids = fields.One2many(comodel_name="invoice.detail", inverse_name="invoice_id")
    payment_ids = fields.One2many(comodel_name="arc.payment", inverse_name="invoice_id")
    comment = fields.Text(string="Comment")

    sub_total_amount = fields.Float(string="Sub Total", default=0.0)
    discount_amount = fields.Float(string="Discount Amount", default=0.0)
    tax_amount = fields.Float(string="Round-Off", default=0.0)
    round_off = fields.Float(string="Round-Off", default=0.0)
    grand_amount = fields.Float(string="Round-Off", default=0.0)

    cgst = fields.Float(string="CGST", default=0.0)
    sgst = fields.Float(string="SGST", default=0.0)
    igst = fields.Float(string="IGST", default=0.0)

    file_name = fields.Char(string="File Name", default="Invoice.pdf")
    report_pdf = fields.Binary(string="Report")

    @api.multi
    def _get_payment_progress(self):
        for rec in self:
            rec_ids = self.env["arc.payment"].search([("invoice_id", "=", rec.id)])
            amount = 0
            if rec_ids:
                amount = sum(rec_ids.mapped("amount"))

            if amount == rec.grand_amount:
                rec.payment_progress = "paid"
            elif amount > 0:
                rec.payment_progress = "partially_paid"
            elif amount == 0:
                rec.payment_progress = "un_paid"

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
            'context': {'default_person_id': self.person_id.id,
                        'default_ref': self.name,
                        'default_amount': self.grand_amount,
                        'default_invoice_id': self.id},
        }

    @api.multi
    def trigger_update_total(self):
        recs = self.detail_ids

        sub_total_amount = cgst = sgst = igst = tax_amount = discount_amount = 0
        for rec in recs:
            rec.update_total()
            cgst = cgst + rec.cgst
            sgst = sgst + rec.sgst
            igst = igst + rec.igst
            sub_total_amount = sub_total_amount + rec.total
            tax_amount = tax_amount + rec.tax_amount
            discount_amount = discount_amount + rec.discount_amount

        total = sub_total_amount
        self.grand_amount = round(total)
        self.round_off = round(total) - total
        self.cgst = cgst
        self.sgst = sgst
        self.igst = igst
        self.sub_total_amount = sub_total_amount
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount

    @api.multi
    def trigger_stock_move(self):
        if self.invoice_type == "pharmacy":
            source_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])
            destination_id = self.env["arc.location"].search([("location_uid", "=", "VIRTUAL OUT")])
        elif self.invoice_type == "purchase":
            source_id = self.env["arc.location"].search([("location_uid", "=", "VIRTUAL IN")])
            destination_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])

        if self.invoice_type in ["pharmacy", "purchase"]:
            for rec in self.detail_ids:
                self.env["arc.move"].create({"date": self.date,
                                             "product_id": rec.product_id.id,
                                             "batch_id": rec.batch_id.id,
                                             "quantity": rec.quantity,
                                             "source_id": source_id.id,
                                             "destination_id": destination_id.id,
                                             "progress": "moved",
                                             "ref": self.name})

    @api.multi
    def trigger_confirm(self):
        self.trigger_update_total()
        self.write({"progress": "confirmed"})

    @api.multi
    def trigger_approve(self):
        self.trigger_update_total()
        self.trigger_stock_move()
        self.write({"progress": "approved"})

    @api.model
    def create(self, vals):
        sequence = "{0}.{1}".format(self._name, vals["invoice_type"])
        vals["name"] = self.env["ir.sequence"].next_by_code(sequence)
        return super(Invoice, self).create(vals)

    @api.multi
    def trigger_treatment_invoice(self):
        record_id = self.env["arc.template"].search([("template_uid", "=", "TREATMENT")])

        data_table = ""

        for rec in self.detail_ids:
            data_table = """{0}<tr><td>{1}</td>"
                                        <td>{2}</td>
                                        <td>{3}</td>
                                        <td>{4}</td>
                                        <td>{5}</td></tr>""".format(data_table,
                                                                    rec.fee_id.name,
                                                                    rec.mrp,
                                                                    rec.discount,
                                                                    rec.tax_id.name_get()[0][1],
                                                                    rec.total)

        data_dict = {"company_logo": "data:image/png;base64,{0}".format(self.company_id.logo),
                     "company_name": self.company_id.name if self.company_id.name else "",
                     "company_address": self.company_id.address if self.company_id.address else "",
                     "patient_name": self.person_id.name if self.person_id.name else "",
                     "patient_id": self.person_id.person_uid if self.person_id.person_uid else "",
                     "patient_address": self.person_id.address(),
                     "info_no": self.name if self.name else "",
                     "info_date": self.date if self.date else "",
                     "data_table": data_table,
                     "sgst": self.sgst,
                     "cgst": self.cgst,
                     "igst": self.igst,
                     "sub_total_amount": self.sub_total_amount,
                     "discount_amount": self.discount_amount,
                     "tax_amount": self.tax_amount,
                     "round_off": self.round_off,
                     "grand_amount": self.grand_amount
                     }

        html_data = record_id.template.format(**data_dict)

        pdfkit.from_string(html_data, '/opt/kon/out.pdf', css="/opt/hospital/static/src/css/template.css")
        pdf_file = open('/opt/kon/out.pdf', 'rb')
        pdf_data = pdf_file.read()
        pdf_file.close()
        out = base64.b64encode(pdf_data)

        self.write({'report_pdf': out, 'file_name': 'treatment_bill.pdf'})

        return {
            'type': 'ir.actions.act_url',
            'url': '/hospital/invoice?model=arc.invoice&id=%s' % (self.id),
            'target': 'new',
        }

    @api.multi
    def trigger_purchase_invoice(self):
        record_id = self.env["arc.template"].search([("template_uid", "=", "PURCHASE")])

        data_table = ""

        for rec in self.detail_ids:
            data_table = """{0}<tr><td>{1}</td>"
                                        <td>{2}</td>
                                        <td>{3}</td>
                                        <td>{4}</td>
                                        <td>{5}</td>
                                        <td>{6}</td></tr>""".format(data_table,
                                                                    rec.product_id.name,
                                                                    rec.mrp,
                                                                    rec.quantity,
                                                                    rec.discount,
                                                                    rec.tax_id.name_get()[0][1],
                                                                    rec.total)

        data_dict = {"company_logo": "data:image/png;base64,{0}".format(self.company_id.logo),
                     "company_name": self.company_id.name if self.company_id.name else "",
                     "company_address": self.company_id.address if self.company_id.address else "",
                     "patient_name": self.person_id.name if self.person_id.name else "",
                     "patient_id": self.person_id.person_uid if self.person_id.person_uid else "",
                     "patient_address": self.person_id.address(),
                     "info_no": self.name if self.name else "",
                     "info_date": self.date if self.date else "",
                     "data_table": data_table,
                     "sgst": self.sgst,
                     "cgst": self.cgst,
                     "igst": self.igst,
                     "sub_total_amount": self.sub_total_amount,
                     "discount_amount": self.discount_amount,
                     "tax_amount": self.tax_amount,
                     "round_off": self.round_off,
                     "grand_amount": self.grand_amount}

        html_data = record_id.template.format(**data_dict)

        pdfkit.from_string(html_data, '/opt/kon/out.pdf', css="/opt/hospital/static/src/css/template.css")
        pdf_file = open('/opt/kon/out.pdf', 'rb')
        pdf_data = pdf_file.read()
        pdf_file.close()
        out = base64.b64encode(pdf_data)

        self.write({'report_pdf': out, 'file_name': 'purchase.pdf'})

        return {
            'type': 'ir.actions.act_url',
            'url': '/hospital/invoice?model=arc.invoice&id=%s' % (self.id),
            'target': 'new',
        }

    @api.multi
    def trigger_pharmacy_invoice(self):
        record_id = self.env["arc.template"].search([("template_uid", "=", "PHARMACY INVOICE")])

        data_table = ""

        for rec in self.detail_ids:
            data_table = """{0}<tr><td>{1}</td>"
                                <td>{2}</td>
                                <td>{3}</td>
                                <td>{4}</td>
                                <td>{5}</td>
                                <td>{6}</td></tr>""".format(data_table,
                                                            rec.product_id,
                                                            rec.mrp,
                                                            rec.quantity,
                                                            rec.discount,
                                                            rec.tax_id.name_get()[0][1],
                                                            rec.total)

        data_dict = {"company_logo": "data:image/png;base64,{0}".format(self.company_id.logo),
                     "company_name": self.company_id.name if self.company_id.name else "",
                     "company_address": self.company_id.address if self.company_id.address else "",
                     "patient_name": self.person_id.name if self.person_id.name else "",
                     "patient_id": self.person_id.person_uid if self.person_id.person_uid else "",
                     "patient_address": self.person_id.address(),
                     "info_no": self.name if self.name else "",
                     "info_date": self.date if self.date else "",
                     "data_table": data_table,
                     "sgst": self.sgst,
                     "cgst": self.cgst,
                     "igst": self.igst,
                     "sub_total_amount": self.sub_total_amount,
                     "discount_amount": self.discount_amount,
                     "tax_amount": self.tax_amount,
                     "round_off": self.round_off,
                     "grand_amount": grand_amount}

        html_data = record_id.template.format(**data_dict)

        pdfkit.from_string(html_data, '/opt/kon/out.pdf', css="/opt/hospital/static/src/css/template.css")
        pdf_file = open('/opt/kon/out.pdf', 'rb')
        pdf_data = pdf_file.read()
        pdf_file.close()
        out = base64.b64encode(pdf_data)

        self.write({'report_pdf': out, 'file_name': 'pharmacy.pdf'})

        return {
            'type': 'ir.actions.act_url',
            'url': '/hospital/invoice?model=arc.invoice&id=%s' % (self.id),
            'target': 'new',
        }


class InvoiceDetail(models.Model):
    _name = "invoice.detail"

    fee_id = fields.Many2one(comodel_name="arc.fee", string="Product")
    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
    batch_id = fields.Many2one(comodel_name="arc.batch", string="Batch")
    manufacturing_date = fields.Date(string="Manufacturing Date")
    expiry_date = fields.Date(string="Expiry Date")
    unit_price = fields.Float(string="Unit Price", default=0.0)
    mrp = fields.Float(string="MRP", default=0.0)
    quantity = fields.Float(string="Quantity", default=1.0)
    discount = fields.Float(string="Discount (%)", default=0.0)
    tax_id = fields.Many2one(comodel_name="product.tax", string="Tax", required=True)
    total = fields.Float(string="Total in INR", default=0.0)
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")

    cgst = fields.Float(string="CGST", required=True, readonly=True, default=0.0)
    sgst = fields.Float(string="SGST", required=True, readonly=True, default=0.0)
    igst = fields.Float(string="IGST", required=True, readonly=True, default=0.0)
    discount_amount = fields.Float(string="Discount Amount", required=True, readonly=True, default=0.0)
    after_discount = fields.Float(string="After Discount", required=True, readonly=True, default=0.0)
    tax_amount = fields.Float(string="Tax Amount", required=True, default=0.0)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.onchange('batch_id')
    def update_batch_details(self):
        if self.batch_id and self.product_id:
            self.manufacturing_date = self.batch_id.manufacturing_date
            self.expiry_date = self.batch_id.expiry_date
            self.unit_price = self.batch_id.unit_price
            self.mrp = self.batch_id.mrp

    def update_total(self):
        state_type = "inter"

        vals = self.env["arc.calculation"].get_item_val(self.mrp,
                                                        self.quantity,
                                                        self.discount,
                                                        self.tax_id.rate,
                                                        state_type)

        self.write(vals)


class InvoicePDF(http.Controller):
    _cp_path = '/hospital'

    @http.route('/hospital/invoice', type='http', auth="public")
    def invoice_download(self, **data):
        record_id = http.request.env['arc.invoice'].search([('id', '=', data.get('id'))])
        if record_id:
            filecontent = base64.b64decode(record_id.report_pdf)
            filename = record_id.file_name
            if filecontent and filename:
                return request.make_response(filecontent,
                                             headers=[('Content-Type', 'application/pdf'),
                                                      ('Content-Disposition', content_disposition(filename))])
        return request.not_found()
