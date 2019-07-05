#

from odoo import models, fields, api
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
PROGRESS_INFO = [("draft", "Draft"), ("confirm", "Confirm")]
PAYMENT_INFO = [("un_paid", "Un Paid"), ("partially_paid", "Partially Paid"), ("paid", "Paid")]


class Laboratory(models.Model):
    _name = "arc.lab"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", reauired=True)
    test_ids = fields.One2many(comodel_name="lab.test", inverse_name="laboratory_id", string="Tests")
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    payment_progress = fields.Selection(selection=PAYMENT_INFO, string="Progress", default="un_paid")
    report = fields.Html(string="Report")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    comment = fields.Text(string="Comment")
    report_pdf = fields.Binary(string="Report")
    file_name = fields.Char(string="File Name", default="report.pdf")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.multi
    def trigger_confirm(self):
        self.write({"progress": "confirm"})

    @api.multi
    def trigger_email(self):
        pass

    @api.multi
    def trigger_report(self):
        recs = self.test_ids

        data = ""

        print self.test_ids
        for rec in recs:
            rec.trigger_report()
            data = "{0}{1}".format(data, rec.report)

        self.report = data

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(Laboratory, self).create(vals)
