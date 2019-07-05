#

from odoo import models, fields, api
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
PROGRESS = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved")]
PAYMENT_PROGRESS = [("un_paid", "Un-Paid"), ("partially_paid", "Partially Paid"), ("paid", "Paid")]


class ReportPayment(models.TransientModel):
    _name = "report.payment"

    from_date = fields.Date(string="From Date", default=current_date, required=True)
    till_date = fields.Date(string="Till Date", default=current_date, required=True)
    detail_ids = fields.One2many(comodel_name="report.payment.detail", inverse_name="report_id")
    person_id = fields.Many2one(comodel_name="arc.person", string="Person")

    @api.multi
    def trigger_report(self):
        self.detail_ids.unlink()
        recs = None
        if self.person_id:
            recs = self.env["arc.payment"].search([("date", ">=", self.from_date),
                                                   ("date", "<=", self.till_date),
                                                   ("company_id", "<=", self.env.user.company_id.id),
                                                   ("person_id", "=", self.person_id.id)])
        else:
            recs = self.env["arc.payment"].search([("date", ">=", self.from_date),
                                                   ("date", "<=", self.till_date),
                                                   ("company_id", "<=", self.env.user.company_id.id)])

        data = []
        for rec in recs:
            data.append((0, 0, {"date": rec.date,
                                "name": rec.name,
                                "person_id": rec.person_id.id,
                                "amount": rec.grand_amount}))

        self.detail_ids = data


class ReportPaymentDetail(models.TransientModel):
    _name = "report.payment.detail"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    person_id = fields.Many2one(comodel_name="arc.person", string="Person")
    amount = fields.Float(string="Amount", default=0.0)
    report_id = fields.Many2one(comodel_name="report.payment", string="Payment")
