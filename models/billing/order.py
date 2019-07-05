#

from odoo import models, fields, api
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
PROGRESS = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Order(models.Model):
    _name = "arc.order"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    progress = fields.Selection(selection=PROGRESS, string="Progress", default="draft")
    detail_ids = fields.One2many(comodel_name="order.detail", inverse_name="order_id")
    comment = fields.Text(string="Comment")

    file_name = fields.Char(string="File Name", default="Invoice.pdf")
    report_pdf = fields.Binary(string="Report")

    @api.multi
    def trigger_confirm(self):
        self.write({"progress": "confirmed"})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(Order, self).create(vals)


class OrderDetail(models.Model):
    _name = "order.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=0.0, required=True)
    order_id = fields.Many2one(comodel_name="arc.order", string="Pharmacy")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

