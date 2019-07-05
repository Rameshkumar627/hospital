# -*- coding: utf-8 -*-

from odoo import models, fields


class LabMaster(models.Model):
    _name = "lab.master"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    price = fields.Float(string="Price")
    template = fields.Html(string="Template")
    value_ids = fields.One2many(comodel_name="lab.master.detail.value", inverse_name="lab_id")
    image_ids = fields.One2many(comodel_name="lab.master.detail.image", inverse_name="lab_id")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)


class LabMasterDetailValue(models.Model):
    _name = "lab.master.detail.value"

    name = fields.Char(string="Name")
    lab_id = fields.Many2one(comodel_name="lab.master", string="Lab")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)


class LabMasterDetailImage(models.Model):
    _name = "lab.master.detail.image"

    name = fields.Char(string="Name")
    lab_id = fields.Many2one(comodel_name="lab.master", string="Lab")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

