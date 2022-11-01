# -*- coding: utf-8 -*-

from odoo import fields,models,api

class companylist(models.Model):
	_name = "company.list"
	_description = "The list of the company whose tender is filled!!!"
	_rec_name = "comp_name"


	comp_name = fields.Many2one('new.tender', store = True, string = "Company Name", required = True)
	companies_street = fields.Char(string = " Comapnies Street", related = "comp_name.tend_street", 
		store = True)
	companies_street2 = fields.Char(related = "comp_name.tend_street2", store = True, 
		string = "Companies Street2")
	companies_city = fields.Char(related = "comp_name.tend_city", store = True, 
		string = "Companies City")
	contact_no = fields.Char(string = "Contact Number", required = True)
	email = fields.Char(string = "Companies E-mail Address")

