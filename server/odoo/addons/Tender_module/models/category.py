# -*- coding: utf-8 -*-

from odoo import models,fields, api

class catelog(models.Model):
	
	_name = "catelog.category"
	_description = "This model contains the category list"

	name = fields.Char(string = "category")
	product = fields.Char(string = "Product Name")
	company = fields.Char(string = "Name of vendor company")
	specification = fields.Char(string = "specification")


	@api.model
	def create(self, values):
		if 'name' in values:
			values['name'] = values['name'].upper()
			new_rec = super(catelog, self).create(values)
			return new_rec
		