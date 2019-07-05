# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTax(models.Model):
    _name = "product.tax"

    name = fields.Char(string="Name", required=True)
    tax_uid = fields.Char(string="Code", required=True)
    rate = fields.Float(string="Rate", default=0.0, required=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{0}-{1}%".format(record.name, record.rate)
            result.append((record.id, name))
        return result
