# -*- coding: utf-8 -*-
{
    'name': "RFPs_module",

    'summary': """
        Complete RFPs Management""",

    'description': """
         All About Tender Managment
    """,

    'author': "Er.Pappu and Er.Bhuwan",
    'website': "http://www.greenit.com.np",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','web','mail'],
    
    # always loaded
    'data': [
        #security
        'security/user_group.xml',
        'security/ir.model.access.csv',
        #data
        'data/res_company_data.xml',
        #report
        'report/report_template.xml',
        'report/bank_guarentee_report.xml',
        'report/bank_indemnity_form.xml',
        #view   
        'views/tendermanagment_view.xml',
        'views/category_view.xml',
        'views/companylist_view.xml',
        'views/banklist_view.xml',
        'views/bank_application_form_view.xml',
        'views/bank_application_email.xml',
        'views/vendor_view.xml',
        'views/tenderemail_templet_view.xml',
        'views/email_templet_view.xml',
        'views/notification_email_template.xml',
        'views/res_company_view.xml',
    ],
    'qweb': [

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "auto_install": False,
    "installable": True,
      'application': True,
}