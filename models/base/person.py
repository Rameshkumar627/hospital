# -*- coding: utf-8 -*-

from odoo import models, fields, api, modules
import base64

PERSON_TYPE = [('supplier', 'Supplier'), ('service', 'Service')]


class ArcPerson(models.Model):
    _name = "arc.person"

    name = fields.Char(string="Name", required=True)
    person_uid = fields.Char(string="ID Card No", readonly=True)
    image = fields.Binary(string="Image", default=lambda self: self.get_image_default())
    small_image = fields.Binary(string="Small Image")
    active = fields.Boolean(string="Active", default=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    # Professional Details
    email = fields.Char(string="e-Mail")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")
    whatsapp = fields.Char(string="Whatsapp")
    website = fields.Char(string="Website")
    contact_name = fields.Char(string="Contact Name")
    contact_position = fields.Char(string="Position")

    # Address in Detail
    door_no = fields.Char(string="Door No")
    building_name = fields.Char(string="Building Name")
    street_1 = fields.Char(string="Street 1")
    street_2 = fields.Char(string="Street 2")
    locality = fields.Char(string="locality")
    landmark = fields.Char(string="landmark")
    city = fields.Char(string="City")
    state_id = fields.Many2one(comodel_name="res.country.state", string="State",
                               default=lambda self: self.env.user.company_id.state_id.id)
    country_id = fields.Many2one(comodel_name="res.country", string="Country")
    pin_code = fields.Char(string="Pincode")

    # Filter
    is_employee = fields.Boolean(string="Is Employee")
    is_patient = fields.Boolean(string="Is Patient")

    person_type = fields.Selection(selection=PERSON_TYPE, string="Person Type")

    def get_image_default(self):
        file_path = modules.module.get_resource_path('hospital', 'static/src/image', 'patient.png')
        file_binary = open(file_path, "r").read()
        image = base64.b64encode(file_binary)
        return image

    def address(self):
        data = ""

        if self.door_no:
            data = "{0}<br>{1}</br>".format(data, self.door_no)

        if self.building_name:
            data = "{0}<br>{1}</br>".format(data, self.building_name)

        if self.street_1:
            data = "{0}<br>{1}</br>".format(data, self.street_1)

        if self.street_2:
            data = "{0}<br>{1}</br>".format(data, self.street_2)

        if self.locality:
            data = "{0}<br>{1}</br>".format(data, self.locality)

        if self.landmark:
            data = "{0}<br>{1}</br>".format(data, self.landmark)

        if self.city:
            data = "{0}<br>{1}</br>".format(data, self.city)

        if self.pin_code:
            data = "{0}<br>{1}</br>".format(data, self.pin_code)

        return data

    @api.model
    def create(self, vals):
        if "person_uid" not in vals:
            vals["person_uid"] = self.env["ir.sequence"].next_by_code(self._name)

        return super(ArcPerson, self).create(vals)
