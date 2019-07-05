#

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirm", "Confirmed"), ("approve", "Approve")]
ADJUST_TYPE = [("increase", "Increase"), ("decrease", "Decrease")]
current_date = datetime.now().strftime("%Y-%m-%d")


class StockAdjust(models.Model):
    _name = "stock.adjust"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")
    adjust_type = fields.Selection(selection=ADJUST_TYPE, default="increase", string="Adjust Type", required=True)
    comment = fields.Text(string="Comment")
    adjust_ids = fields.One2many(comodel_name="adjust.detail", inverse_name="adjust_id")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.multi
    def trigger_adjust(self):
        if self.adjust_type == "increase":
            source_id = self.env["arc.location"].search([("location_uid", "=", "VIRTUAL IN")])
            destination_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])
        elif self.adjust_type == "decrease":
            source_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])
            destination_id = self.env["arc.location"].search([("location_uid", "=", "VIRTUAL OUT")])

        for rec in self.adjust_ids:
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
        self.write({"progress": "confirm"})

    @api.multi
    def trigger_approve(self):
        self.trigger_adjust()
        self.write({"progress": "approve"})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StockAdjust, self).create(vals)


class AdjustDetail(models.Model):
    _name = "adjust.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)
    batch_id = fields.Many2one(comodel_name="arc.batch", string="Batch", required=True)
    manufacturing_date = fields.Date(string="Manufacturing Date")
    expiry_date = fields.Date(string="Expiry Date")
    unit_price = fields.Float(string="Unit Price", default=0.0, required=True)
    mrp = fields.Float(string="MRP", default=0.0, required=True)
    quantity = fields.Float(string="Quantity", default=0.0, required=True)
    adjust_id = fields.Many2one(comodel_name="stock.adjust", string="Adjust")

    @api.onchange('batch_id')
    def update_batch_details(self):
        if self.batch_id and self.product_id:
            self.manufacturing_date = self.batch_id.manufacturing_date
            self.expiry_date = self.batch_id.expiry_date
            self.unit_price = self.batch_id.unit_price
            self.mrp = self.batch_id.mrp
