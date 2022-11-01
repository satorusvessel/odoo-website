# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VendorProduct(models.Model):
    _name = "vendor.product"
    _description = "All vendor Products"
    _rec_name = "prod_name"

    currency_id = fields.Many2one("res.currency", "Currency", required=True)
    prod_name = fields.Char(string="Product Name", required=True, index=True)
    vendor_name = fields.Char(string="Vendor Name", index=True)
    vendor_email = fields.Char(string="Vendor E-mail")
    pro_category = fields.Char(string="Product Category")
    pro_price = fields.Monetary(string="Sellable Price")
    specification = fields.Text(string="Specification")
    pro_specification = fields.Binary(string="Upload Specification")
    pro_file_name = fields.Char(string="Specification File Name")
    tend_company_name = fields.Many2one("new.tender")

    @api.model
    def create(self, values):
        if "prod_name" and "vendor_name" in values:
            values["prod_name"] = values["prod_name"].upper()
            values["vendor_name"] = values["vendor_name"].upper()
            new_rec = super(VendorProduct, self).create(values)
            return new_rec
            pass

    def write(self, values, context=None):
        if "prod_name" in values:
            values["prod_name"] = values["prod_name"].upper()
            old_rec = super(VendorProduct, self).write(values)
        else:
            old_rec = super(VendorProduct, self).write(values)
            return True
            pass
        pass

    def send_email_template(self):
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            template_obj = ir_model_data.get_object_reference(
                "Tender_module", "req_email_template_id"
            )[1]
        except ValueError:
            template_obj = False
        try:
            compose_form_obj = ir_model_data.get_object_reference(
                "mail", "email_compose_message_wizard_form"
            )[1]
        except ValueError:
            compose_form_obj = False
        ctx = {
            "default_model": "vendor.product",
            "default_res_id": self.ids[0],
            "default_use_template": bool(template_obj),
            "default_template_id": template_obj,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "force_email": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form_obj, "form")],
            "view_id": compose_form_obj,
            "target": "new",
            "context": ctx,
        }
        pass
