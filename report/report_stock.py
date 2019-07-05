#

from odoo import models, fields, api
from datetime import datetime, timedelta

current_date = datetime.now().strftime("%Y-%m-%d")


class ReportStock(models.TransientModel):
    _name = "report.stock"

    from_date = fields.Date(string="From Date", default=current_date, required=True)
    till_date = fields.Date(string="Till Date", default=current_date, required=True)
    detail_ids = fields.One2many(comodel_name="report.stock.detail", inverse_name="report_id")

    @api.multi
    def trigger_report(self):
        self.detail_ids.unlink()
        recs = self.env["arc.product"].search([])
        pharmacy_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])

        from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
        opening_date_obj = from_date - timedelta(days=1)
        opening_date = opening_date_obj.strftime("%Y-%m-%d")

        data = []
        for rec in recs:
            opening = self.env["arc.stock"].get_date_stock(opening_date,
                                                           rec.id,
                                                           pharmacy_id.id)
            closing = self.env["arc.stock"].get_date_stock(self.till_date,
                                                           rec.id,
                                                           pharmacy_id.id)

            data.append((0, 0, {"product_id": rec.id,
                                "opening_stock": opening,
                                "closing_stock": closing}))

        self.detail_ids = data


class ReportStockDetail(models.TransientModel):
    _name = "report.stock.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
    opening_stock = fields.Float(string="Opening Stock", default=0.0)
    closing_stock = fields.Float(string="Closing Stock", default=0.0)
    report_id = fields.Many2one(comodel_name="report.stock", string="Stock")
