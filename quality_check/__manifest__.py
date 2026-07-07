{
    'name': 'Quality Check',
    'version': '19.0.1.0.0',
    'category': 'Quality',
    'summary': 'Simple Quality Check Module',
    'author': 'SQALOGY',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/quality_check_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
