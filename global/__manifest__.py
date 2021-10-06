# -*- coding: utf-8 -*-
{
    'name': "global",

    'summary': """
        Personalizaciones para Global Proteccion
        """,

    'description': """
        Modulo de personalizaciones para Global Proteccion.
    """,

    'author': "TK Analytics",
    'website': "http://www.tkanalytics.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    'application': True,
    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'website_sale', 'purchase', 'stock', 'account_intrastat', 'account', 'sh_message', ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/analytic_account_views.xml',
        'views/stock_picking_views.xml',
        'email_templates/email_templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
