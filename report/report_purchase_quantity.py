#

from odoo import models, fields, api
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
PROGRESS = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved")]
PAYMENT_PROGRESS = [("un_paid", "Un-Paid"), ("partially_paid", "Partially Paid"), ("paid", "Paid")]


class ReportPurchaseQuantity(models.TransientModel):
    _name = "report.purchase.quantity"

    from_date = fields.Date(string="From Date", default=current_date, required=True)
    till_date = fields.Date(string="Till Date", default=current_date, required=True)
    detail_ids = fields.One2many(comodel_name="report.purchase.quantity.detail", inverse_name="report_id")
    person_id = fields.Many2one(comodel_name="arc.person", string="Person")

    @api.multi
    def trigger_report(self):
        self.detail_ids.unlink()
        recs = None
        if self.person_id:
            recs = self.env["invoice.detail"].search([("invoice_id.date", ">=", self.from_date),
                                                      ("invoice_id.date", "<=", self.till_date),
                                                      ("invoice_id.invoice_type", "=", "purchase"),
                                                      ("invoice_id.company_id", "<=", self.env.user.company_id.id),
                                                      ("invoice_id.person_id", "=", self.person_id.id)])
        else:
            recs = self.env["invoice.detail"].search([("invoice_id.date", ">=", self.from_date),
                                                      ("invoice_id.date", "<=", self.till_date),
                                                      ("invoice_id.invoice_type", "=", "purchase"),
                                                      ("invoice_id.company_id", "<=", self.env.user.company_id.id)])

        data = []
        for rec in recs:
            data.append((0, 0, {"date": rec.invoice_id.date,
                                "invoice_id": rec.invoice_id.id,
                                "person_id": rec.invoice_id.person_id.id,
                                "product_id": rec.product_id.id,
                                "batch_id": rec.batch_id.id,
                                "manufacturing_date": rec.manufacturing_date,
                                "expiry_date": rec.expiry_date,
                                "unit_price": rec.unit_price,
                                "mrp": rec.mrp,
                                "quantity": rec.quantity,
                                "discount": rec.discount,
                                "tax_id": rec.tax_id.id,
                                "total": rec.total}))

        self.detail_ids = data


class ReportPurchaseQuantityDetail(models.TransientModel):
    _name = "report.purchase.quantity.detail"

    date = fields.Date(string="Date")
    person_id = fields.Many2one(comodel_name="arc.person", string="Person")
    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
    batch_id = fields.Many2one(comodel_name="arc.batch", string="Batch")
    manufacturing_date = fields.Date(string="Manufacturing Date")
    expiry_date = fields.Date(string="Expiry Date")
    unit_price = fields.Float(string="Unit Price", default=0.0)
    mrp = fields.Float(string="MRP", default=0.0)
    quantity = fields.Float(string="Quantity", default=0.0)
    discount = fields.Float(string="Discount (%)", default=0.0)
    tax_id = fields.Many2one(comodel_name="product.tax", string="Tax")
    total = fields.Float(string="Total in INR", default=0.0)
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    report_id = fields.Many2one(comodel_name="report.purchase.quantity", string="Purchase")
