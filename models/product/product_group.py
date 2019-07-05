#

from odoo import models, fields


class ProductGroup(models.Model):
    _name = "product.group"

    name = fields.Char(string="Name", required=True)
    group_uid = fields.Char(string="Code", required=True)
    sub_group_ids = fields.One2many(comodel_name="product.sub.group", inverse_name="group_id")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

