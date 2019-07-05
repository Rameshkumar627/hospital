# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("discharge", "Discharge")]
PATIENT_STATUS = [("normal", "Normal"), ("emergency", "Emergency")]
RELATION_INFO = [('father', 'Father'),
                 ('mother', 'Mother'),
                 ('wife', 'Wife'),
                 ('friend', 'Friend'),
                 ('brother', 'Brother'),
                 ('sister', 'Sister'),
                 ('uncle', 'Uncle'),
                 ('aunt', 'Aunt'),
                 ('grand_father', 'Grand Father'),
                 ('grand_mother', 'Grand Mother'),
                 ('son', 'Son'),
                 ('daughter', 'Daughter'),
                 ('other', 'Other')]
current_date = datetime.now().strftime("%Y-%m-%d")


class Discharge(models.Model):
    _name = "arc.discharge"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    image = fields.Binary(string="Image")
    date = fields.Date(string="Date", default=current_date, required=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    treatment_id = fields.Many2one(comodel_name="ipd.treatment", string="Treatment", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    # Admission Detail
    reason_id = fields.Many2one(comodel_name="discharge.reason", string="Reason", required=True)
    reason_detail = fields.Text(string="Reason in detail")
    contact_person = fields.Char(string="Contact Person")
    relation = fields.Selection(selection=RELATION_INFO, string="Relation")
    mobile_1 = fields.Char(string="Mobile 1")
    mobile_2 = fields.Char(string="Mobile 2")
    address = fields.Text(string="Address")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    comment = fields.Text(string="Comment")
    patient_status = fields.Selection(selection=PATIENT_STATUS, default="normal", string="Patient Status")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")

    @api.multi
    def trigger_discharge(self):
        self.write({"progress": "discharge"})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(Discharge, self).create(vals)
