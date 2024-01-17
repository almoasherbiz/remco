{
    'name': "Transaction Payments Without HR",
    'summary': """Transaction Payments Without HR""",
    'description': """Transaction Payments Without HR""",
    'author': "Marwa Abouzaid",
    'website': "http://almoasherbiz.com/",
    'category': 'Uncategorized',
    'version': '15.0.1.1.1',
    'depends': ['base','account','account_accountant'],
    'data': [
        'security/ir.model.access.csv',
        'views/transaction_views.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,

}
