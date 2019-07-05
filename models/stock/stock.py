# -*- coding: utf-8 -*-

from odoo import models


# Stock
class ArcStock(models.Model):
    _name = "arc.stock"

    def get_current_stock(self, product_id, location_id, batch_id):
        source_ids = self.env["arc.move"].search([("product_id", "=", product_id),
                                                  ("source_id", "=", location_id),
                                                  ("batch_id", "=", batch_id),
                                                  ("progress", "=", "moved")])

        destination_ids = self.env["arc.move"].search([("product_id", "=", product_id),
                                                       ("destination_id", "=", location_id),
                                                       ("batch_id", "=", batch_id),
                                                       ("progress", "=", "moved")])

        quantity_in = sum(source_ids.mapped("quantity"))
        quantity_out = sum(destination_ids.mapped("quantity"))

        return quantity_out - quantity_in

    def get_date_stock(self, date, product_id, location_id):
        source_ids = self.env["arc.move"].search([("date", "<=", date),
                                                  ("product_id", "=", product_id),
                                                  ("source_id", "=", location_id),
                                                  ("progress", "=", "moved")])

        destination_ids = self.env["arc.move"].search([("date", "<=", date),
                                                       ("product_id", "=", product_id),
                                                       ("destination_id", "=", location_id),
                                                       ("progress", "=", "moved")])

        quantity_in = sum(source_ids.mapped("quantity"))
        quantity_out = sum(destination_ids.mapped("quantity"))

        return quantity_out - quantity_in

