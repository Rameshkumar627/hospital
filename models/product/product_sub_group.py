#

from odoo import models, fields


class ProductSubGroup(models.Model):
    _name = "product.sub.group"

    name = fields.Char(string="Name", required=True)
    sub_group_uid = fields.Char(string="Code", required=True)
    group_id = fields.Many2one(comodel_name="product.group", string="Product Group", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

