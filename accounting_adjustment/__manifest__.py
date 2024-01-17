# -*- coding: utf-8 -*-
{
    'name': "Accounting Adjustment",

    'summary': """
        Accounting Adjustment""",

    'description': """
        
    """,
    'author': "Marwa Abouzaid",
    'category': 'account',
    'version': '16.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_accountant', 'account_reports'],

    # always loaded
    'data': [
        'views/customer_view.xml',
        'reports/partner_ledger_report.xml',
        'reports/invoice_report.xml',
    ],

}