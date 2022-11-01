# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import datetime
import base64
from werkzeug.urls import url_encode

# from odoo.addons import decimal_precision as dp


class NewTender(models.Model):
    _name = "new.tender"
    _description = "All About Managment of Tender Notice"
    _order = "name, subm_date"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name of Company",
        required=True,
        search="_search_name",
        index=True,
        track_visibility=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    tend_street = fields.Char(
        string="Street",
        required=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    tend_street2 = fields.Char(
        string="Street2",
        index=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    tend_city = fields.Char(
        string="City",
        required=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    category = fields.Many2one(
        "catelog.category",
        string="Bid Title",
        required=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    publ_date = fields.Datetime(
        string="Tender Published Date",
        required=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    pre_bid = fields.Datetime(
        string="Pre-Bid Meeting",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    pre_bid_location = fields.Char(
        string="Location",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    # selection between days and date in tender dates
    field_type = fields.Selection(
        [("days", "Days"), ("date", "Date")],
        "Tender Submisson",
        default="date",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    subm_days = fields.Integer(
        string="Expiry Days",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    subm_date = fields.Datetime(
        string="Tender Submisson Date",
        required=True,
        index=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    days_left = fields.Char(
        string="Remaining Days",
        compute="_check_days",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    tender_expire = fields.Integer(default=0)
    bid_open_tech = fields.Datetime(
        "Technical",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    bid_open_fina = fields.Datetime(
        "Financial",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    # condition for percent or amount
    bond_amount_type = fields.Selection(
        [("percentage", "Percentage"), ("amount", "Amount")],
        string="Bid Bond Type",
        default="amount",
        store=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    percentage = fields.Float(
        digits="Percentage",
        default=0.0,
        required=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
        help="The percentage value should be in Decimal",
    )
    amount = fields.Float(
        string="Bid Security",
        required=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    bid_amount = fields.Float(string="Bond Amount/Percentage", compute="_check_value")
    bid_validity = fields.Date(
        string="Bid Security Validity",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    bid_validity_days = fields.Char(compute="_check_validity")
    # condition for percent or amount
    perform_bond_type = fields.Selection(
        [("perform_bond_percent", "Percentage"), ("perform_bond_amount", "Amount")],
        string="Performance Bond Type",
        default="perform_bond_percent",
        store=True,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    perform_bond_amount = fields.Float(
        string="Performance Security Amount",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    perform_bond_percent = fields.Float(
        digits="Percentage",
        default=0.0,
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    perform_bond_show = fields.Float(compute="_check_perform_value")
    image = fields.Binary(
        string="Tender Notice Image",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    state = fields.Selection(
        [
            ("record", "Record"),
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("done", "Locked"),
            ("tendered", "Tendered"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        copy=False,
        track_visibility="onchange",
        default="record",
    )
    # calling the notebook page
    myprod_id = fields.One2many(
        "tender.product",
        "product_parent",
        string="Order Products",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
        copy=True,
        auto_join=True,
    )

    note = fields.Text(
        string="Notes",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    upload_file = fields.Binary(
        string="Upload File",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    file_name = fields.Char(
        string="File Name",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    bank_id = fields.Boolean(
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]}
    )
    contract_id = fields.Char(
        string="IFB/Contract No. and Date",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    bid_doc_type = fields.Selection(
        [("online", "e-Bidding"), ("paperbased", "HardCopy")],
        "Bidding Option",
        default="paperbased",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )
    bid_doc_price = fields.Float(
        string="Amount of Bidding Document",
        states={"cancel": [("readonly", True)], "done": [("readonly", True)]},
    )

    def unlink(self):
        for tender in self:
            if tender.state not in ("record", "cancel"):
                raise UserError(
                    "You can not delete a confirmed quotation or a record whose docs are requested. You must first cancel it."
                )
            return super(NewTender, self).unlink()

    pass

    @api.constrains("publ_date", "subm_date")
    def _check_date(self):
        if self.subm_date < self.publ_date:
            raise ValidationError(
                "The submisson date should be geater then published date!!!"
            )
            pass

    @api.model
    @api.onchange("publ_date", "subm_days")
    def _calculate_date(self):
        if self.publ_date and self.subm_days:
            planned = self.publ_date + datetime.timedelta(days=self.subm_days)
            self.subm_date = planned

    @api.depends("subm_date")
    def _check_days(self):
        if self.subm_date:
            current_date = datetime.datetime.now()
            rdy = self.subm_date - current_date
            self.days_left = rdy.days + 1
        if int(self.days_left) < int(self.tender_expire):
            expire = "Tender is Expired"
            self.days_left = expire
        pass

    @api.depends("bid_validity")
    def _check_validity(self):
        if self.bid_validity:
            # current_date = datetime.datetime.now().strptime('2019-05-03','%Y-%m-%d')
            current_date = fields.Date.today()
            validity = self.bid_validity - current_date
            self.bid_validity_days = validity.days + 1
        if int(self.bid_validity_days) < 0:
            self.bid_validity_days = "Validity of Security Bond is Expired."

    @api.constrains("percentage")
    def _check_percentage(self):
        if self.percentage > 100 or self.percentage < 0:
            raise ValidationError(
                "The percentage cannot be negative or greater than 100!!!"
            )

    @api.model
    @api.onchange("percentage", "amount")
    def _check_value(self):
        for each in self:
            each.bid_amount = each.percentage or each.amount

    pass

    @api.constrains("perform_bond_percent")
    def _check_perform_bond_percent(self):
        if self.perform_bond_percent > 100 or self.perform_bond_percent < 0:
            raise ValidationError(
                "The percentage cannot be negative or greater than 100!!"
            )

    @api.model
    @api.onchange("perform_bond_amount", "perform_bond_percent")
    def _check_perform_value(self):
        for perform_each in self:
            perform_each.perform_bond_show = (
                perform_each.perform_bond_percent or perform_each.perform_bond_amount
            )

    # To send mail on creation of a new record
    @api.model
    def create(self, values):
        if "name" and "tend_street" and "tend_city" in values:
            values["name"] = values["name"].title()
            values["tend_street"] = values["tend_street"].title()
            values["tend_city"] = values["tend_city"].title()
            rec = super(NewTender, self).create(values)
            # here "rec" is an id that gets value from the action_mail_send
            template = self.env.ref("Tender_module.notification_email_template_id")
            template.send_mail(rec.id, force_send=True)
            # rec.action_mail_send()
            return rec

    # To access all the group users to send mail
    def task_send_mail(self):
        user_group = self.env.ref("Tender_module.group_user")
        email_list = [
            user.partner_id.email for user in user_group.users if user.partner_id.email
        ]
        return ",".join(email_list)

    # To send the link to access the tender Record
    def action_mail_send(self):
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        url_params = {
            "id": self.id,
            "action": self.env.ref("Tender_module.action_record_form").id,
            "model": "new.tender",
            "view_type": "form",
            "menu_id": self.env.ref("Tender_module.tender_menu_record").id,
        }
        params = "/web?#%s" % url_encode(url_params)
        param = base_url + params
        return param

    # send email with a pop-up to edit the template
    def send_mail_template(self):
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            template_id = ir_model_data.get_object_reference(
                "Tender_module", "tenderemail_templet"
            )[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                "mail", "email_compose_message_wizard_form"
            )[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            "default_model": "new.tender",
            "default_res_id": self.ids[0],
            "default_use_template": bool(template_id),
            "default_template_id": template_id,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "force_email": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form_id, "form")],
            "view_id": compose_form_id,
            "target": "new",
            "context": ctx,
        }
        pass

    def action_cancel(self):
        return self.write({"state": "cancel"})
        pass

    def action_record(self):
        return self.write({"state": "record"})
        pass

    def action_done(self):
        return self.write({"state": "done"})
        pass

    def action_unlock(self):
        self.write({"state": "tendered"})
        pass

    def action_confirm(self):
        return self.write({"state": "draft"})
        pass

    def action_email_send(self):
        return self.write({"state": "sent"})
        pass


# The notebook page model
class myproduct(models.Model):
    _name = "tender.product"
    _description = "Product order line"

    product_parent = fields.Many2one("new.tender", string="Order", ondelete="restrict")
    prod_id = fields.Many2one("vendor.product", string="Product Name", required=True)
    specification = fields.Text(
        string="Description", store=True, related="prod_id.specification"
    )
    qty = fields.Float(string="Required Qty")
    currency_id = fields.Many2one(related="prod_id.currency_id", store=True)
    rate = fields.Monetary(string="Unit Price", store=True, related="prod_id.pro_price")
    maf = fields.Boolean(string="MAF")
    total = fields.Monetary(string="Total Price", compute="compute_unit_total")

    @api.model
    @api.depends("qty", "rate")
    def compute_unit_total(self):
        for linesvalue in self:
            if linesvalue.qty and linesvalue.rate:
                amount = linesvalue.qty * linesvalue.rate
                linesvalue.total = amount
            else:
                linesvalue.total = 0.0
