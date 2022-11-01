# -*- coding: utf-8 -*-

from num2words import num2words
from odoo import api, fields, models


class BankGuarantee(models.Model):
    _name = "bank.guarantee"
    _description = "Bank Guarantee Application Form"
    _rec_name = "bank_name"

    bank_name = fields.Many2one("banks.list")
    branch = fields.Char(store=True, related="bank_name.bank_street")
    date = fields.Date(string="Date:")
    parent_id = fields.Many2one("res.company", string="Name of Applicant", index=True)
    add_street = fields.Char(related="parent_id.company_street", store=True)
    add_street2 = fields.Char(related="parent_id.company_street2", store=True)
    add_city = fields.Char(related="parent_id.company_city", store=True)
    add_phone = fields.Char(related="parent_id.company_phone", store=True)
    tender_id = fields.Many2one("new.tender", string="Name of Beneficiary")
    tender_street = fields.Char(related="tender_id.tend_street", store=True)
    tender_street2 = fields.Char(related="tender_id.tend_street2", store=True)
    tender_city = fields.Char(related="tender_id.tend_city", store=True)
    nature1 = fields.Boolean(string="Bid Bond")
    nature2 = fields.Boolean(string="Performance Bond")
    nature3 = fields.Boolean(string="Advance Payment Guarantee")
    nature4 = fields.Boolean(string="Others(Specify)")
    bond_selection = fields.Selection(related="tender_id.bond_amount_type", store=True)
    amount = fields.Float(related="tender_id.amount", store=True)
    percentage = fields.Float(related="tender_id.percentage", store=True)
    bid_amount_value = fields.Float(related="tender_id.bid_amount", store=True)
    amt_inwords = fields.Text(compute="set_amt_in_words")
    Performance_selection = fields.Selection(
        related="tender_id.perform_bond_type", store=True
    )
    perform_bond_amount = fields.Float(
        related="tender_id.perform_bond_amount", store=True
    )
    perform_bond_percent = fields.Float(
        related="tender_id.perform_bond_percent", store=True
    )
    amount_inwords = fields.Text(compute="amount_into_text")
    bond_validity_from = fields.Date(string="Validity of Bond")
    bond_validity_to = fields.Date(string="Validity Up To")
    purpose = fields.Many2one(
        related="tender_id.category", store=True, string="Contract(Purpose)"
    )
    contract_no = fields.Char(related="tender_id.contract_id", store=True)
    contract_paper1 = fields.Boolean(string="Enclosed")
    contract_paper2 = fields.Boolean(string="Not Enclosed")
    counter_guarentee1 = fields.Boolean(string="Not Furnished")
    counter_guarentee2 = fields.Boolean(string="Will be Furnished")
    account_no = fields.Char(string="Bank Account No:")
    stamp = fields.Binary(string="Company Stamp")
    auth_signature = fields.Binary()
    currency_id = fields.Many2one(
        "res.currency", related="parent_id.currency_id", store=True, string="Currency"
    )

    @api.depends("amount")
    def set_amt_in_words(self):
        self.amt_inwords = (
            self.env.ref("base.NPR")
            .with_context({"lang": "en_US"})
            .amount_to_text(self.amount)
        )
        self.amt_inwords += "\tOnly."

    @api.depends("perform_bond_amount")
    def amount_into_text(self):
        self.amount_inwords = (
            self.env.ref("base.NPR")
            .with_context({"lang": "en_US"})
            .amount_to_text(self.perform_bond_amount)
        )
        self.amount_inwords += "\tOnly."

    # send email with a pop-up to edit the template
    def reqst_bank_guarantee(self):
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            template_bank_id = ir_model_data.get_object_reference(
                "Tender_module", "bank_gearantee_request_email"
            )[1]
        except ValueError:
            template_bank_id = False
        try:
            compose_bank_form_id = ir_model_data.get_object_reference(
                "mail", "email_compose_message_wizard_form"
            )[1]
        except ValueError:
            compose_bank_form_id = False
        ctx = {
            "default_model": "bank.guarantee",
            "default_res_id": self.ids[0],
            "default_use_template": bool(template_bank_id),
            "default_template_id": template_bank_id,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "force_email": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_bank_form_id, "form")],
            "view_id": compose_bank_form_id,
            "target": "new",
            "context": ctx,
        }
        pass
