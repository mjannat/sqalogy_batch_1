# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QualityCheck(models.Model):
    _name = "quality.check"
    _description = "Quality Control Check"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"
    _rec_name = "name"

    # ==========================================
    # FIELD DEFINITIONS
    # ==========================================
    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )
    product_name = fields.Char(
        string="Product",
        required=True,
        tracking=True,
    )
    inspector_id = fields.Many2one(
        comodel_name="res.users",
        string="Main Inspector",
        default=lambda self: self.env.user,
        tracking=True,
    )
    additional_inspector_ids = fields.Many2many(
        comodel_name="res.users",
        string="Additional Inspectors",
    )
    check_date = fields.Date(
        string="Check Date",
        default=fields.Date.today,
    )
    quantity = fields.Float(
        string="Quantity",
    )
    remarks = fields.Text(
        string="Remarks",
    )
    result = fields.Selection(
        selection=[
            ("pass", "Pass"),
            ("fail", "Fail"),
        ],
        string="Result",
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )
    quantity_lines = fields.One2many('quality.check.line', 'line_id','Product Line')

    # ==========================================
    # ORM OVERRIDES
    # ==========================================
    @api.model
    def create(self, vals_list):
        """Generates sequence reference number on creation."""
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                seq_code = "quality.check.code"
                vals["name"] = self.env["ir.sequence"].next_by_code(seq_code) or "New"
        return super(QualityCheck, self).create(vals_list)

    # ==========================================
    # BUSINESS ACTIONS
    # ==========================================
    def action_confirm(self):
        """Moves the state to confirmed."""
        for record in self:
            record.state = "confirmed"

    def action_done(self):
        """Validates result and sets state to done."""
        for record in self:
            if not record.result:
                raise ValidationError("Please select Pass or Fail before completion.")
            record.state = "done"