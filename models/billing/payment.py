#

from odoo import models, fields, api, exceptions
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
TRANSACTION_TYPE = [("cash", "Cash"), ("bank", "Bank")]
TRANSACTION_CATEGORY = [("credit_debit_card", "Credit/ Debit Card"),
                        ("paytm", "Paytm"),
                        ("google_pay", "Google Pay")]


class Payment(models.Model):
    _name = "arc.payment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Person", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    amount = fields.Float(string="Amount", default=0.0)
    transaction_type = fields.Selection(selection=TRANSACTION_TYPE, string="Payment")
    transaction_category = fields.Selection(selection=TRANSACTION_CATEGORY, string="Payment Category")
    comment = fields.Text(string="Comment")
    ref = fields.Char(string="Ref")
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")

    @api.model
    def create(self, vals):
        if "invoice_id" in vals:
            invoice_id = self.env["arc.invoice"].search([("id", "=", vals["invoice_id"])])

            if invoice_id.grand_amount < vals["amount"]:
                raise exceptions.ValidationError("Error! Payment amount is greater than invoice amount")

        return super(Payment, self).create(vals)
