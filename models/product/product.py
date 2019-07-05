#

from odoo import models, fields, api


class Product(models.Model):
    _name = "arc.product"

    name = fields.Char(string="Name", required=True)
    product_uid = fields.Char(string="Code", readonly=True)
    group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group", required=True)
    image = fields.Binary(string="Image")
    description = fields.Text(string="Description")
    comment = fields.Text(string="Comment")
    batch_ids = fields.One2many(comodel_name="arc.batch", inverse_name="product_id")
    hsn_code = fields.Char(string="HSN Code")
    quantity = fields.Float(string="Quantity", compute="get_quantity")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    @api.multi
    def get_quantity(self):
        for rec in self:
            batch_ids = rec.batch_ids

            rec.quantity = sum(batch_ids.mapped("quantity"))

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.product_uid, record.name)
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        group_id = self.env["product.group"].search([("id", "=", vals["group_id"])])
        sub_group_id = self.env["product.sub.group"].search([("id", "=", vals["sub_group_id"])])
        sequence = self.env["ir.sequence"].next_by_code(self._name)

        vals["product_uid"] = "{0}/{1}/{2}".format(group_id.group_uid, sub_group_id.sub_group_uid, sequence)

        return super(Product, self).create(vals)
