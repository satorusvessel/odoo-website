# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BankList(models.Model):
	_name = "banks.list"
	_description = "The list of the banks for Bank security"


	name = fields.Char(required = True)
	bank_street = fields.Char(required = True)
	bank_city = fields.Char(string = "City", required = True)
	bank_contact_number = fields.Char(string = "Contact Number")
	bank_email_address = fields.Char(string = "Email Address", required = True)


	@api.model 
	def create(self,values):
		if 'name' and 'bank_street' and 'bank_city' in values:
			values['name'] = values['name'].title()
			values['bank_street'] = values['bank_street'].title()
			values['bank_city'] = values['bank_city'].title()
			edit_rec = super(BankList, self).create(values)
			return edit_rec