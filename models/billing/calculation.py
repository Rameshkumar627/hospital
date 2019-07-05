# -*- coding: utf-8 -*-

from odoo import models


class Calculation(models.Model):
    _name = "arc.calculation"

    def get_item_val(self, unit_price, quantity, discount, tax_rate, tax_type):
        product_value = unit_price * quantity
        discount_amount = product_value * (discount/100)
        after_discount = product_value - discount_amount
        tax_amount = (product_value - discount_amount) * (tax_rate/100)
        total = product_value - discount_amount + tax_amount

        cgst = sgst = igst = 0
        if tax_type == "inter":
            cgst = sgst = tax_amount/2
        elif tax_type == "outer":
            igst = tax_amount

        vals = {"unit_price": unit_price,
                "quantity": quantity,
                "discount": discount,
                "tax_rate": tax_rate,
                "cgst": cgst,
                "sgst": sgst,
                "igst": igst,
                "discount_amount": discount_amount,
                "tax_amount": tax_amount,
                "after_discount": after_discount,
                "total": total,
                }

        return vals
