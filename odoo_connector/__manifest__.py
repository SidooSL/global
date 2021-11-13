# -*- coding: utf-8 -*-
{
    'name': "Odoo(SH) Connector ",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Techneith",
    'website': "http://www.techneith.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/templates.xml',
        'views/views.xml',
        'data/scheduler.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
