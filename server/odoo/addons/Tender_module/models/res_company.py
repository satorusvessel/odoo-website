#-*- coding: utf-8 -*-

from odoo import api, fields, models

class Company(models.Model):
	_inherit = "res.company"

	company_street = fields.Char(string = "Street")
	company_street2 = fields.Char(string = "Street2")
	company_zip = fields.Char(string = "Zip")
	company_city = fields.Char(string = "City")
	
	company_email = fields.Char(string = "Company Email")
	company_phone = fields.Char(string = "Phone No.")
	company_website = fields.Char(string = "Website")
	company_vat = fields.Char(string = "Vat ID")
	company_registry = fields.Char(string = "Company Registry")
	company_twitter = fields.Char(string = "Twitter Account")
	company_facebook =fields.Char(string = "Facebook Account")
	company_github =fields.Char(string = "Github Account")