#

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
current_date = datetime.now().strftime("%Y-%m-%d")


class StockMove(models.Model):
    _name = "arc.move"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
    batch_id = fields.Many2one(comodel_name="arc.batch", string="Batch")
    description = fields.Text(string="Description")
    quantity = fields.Float(string="Quantity", default=0.0)
    source_id = fields.Many2one(comodel_name="arc.location", string="Source")
    destination_id = fields.Many2one(comodel_name="arc.location", string="Destination")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")
    comment = fields.Text(string="Comment")
    ref = fields.Char(string="Ref")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.constrains("source_id", "product_id")
    def check_current_stock(self):
        if self.source_id.location_uid == "PHARMACY":
            current_stock = self.env["arc.stock"].get_current_stock(self.product_id.id,
                                                                    self.source_id.id,
                                                                    self.batch_id.id)

            if current_stock < 0:
                raise exceptions.ValidationError("Error! Please check stock")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StockMove, self).create(vals)