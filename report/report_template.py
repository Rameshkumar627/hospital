#

from odoo import models, fields, api


class ArcTemplate(models.Model):
    _name = "arc.template"

    name = fields.Char(string="Name")
    template_uid = fields.Char(string="Code")
    template = fields.Html(string="Template")
