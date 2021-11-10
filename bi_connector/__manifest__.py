# -*- coding: utf-8 -*-
{
    'name': "Power BI / Tableau Odoo BI Connector",

    'summary': """
        Power BI and Tableau are widely accepted business intelligence tool which helps businesses analyse their data in forms of illustrative graphs and charts. It enables one to make sense of data, get deeper insights into data and improvise on business strategies. If you are having an ERP system like Odoo to encapsulate all the business workflows in digital form, Power BI, Tableau or any BI tool such as Metabase, Sisense, Qlik view, Datapine, Cognos, Pentaho, Domo etc can really come in handy to analyse the historical data of Sales, CRM, Profit and Loss analysis, etc.""",

    'description': """
        Power BI and Tableau are widely accepted business intelligence tool which helps businesses analyse their data in forms of illustrative graphs and charts. It enables one to make sense of data, get deeper insights into data and improvise on business strategies. If you are having an ERP system like Odoo to encapsulate all the business workflows in digital form, Power BI, Tableau or any BI tool such as Metabase, Sisense, Qlik view, Datapine, Cognos, Pentaho, Domo etc can really come in handy to analyse the historical data of Sales, CRM, Profit and Loss analysis, etc.
    """,

    'author': "Techneith",
    'website': "https://techneith.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Connector',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    
    'images': ['static/description/banner.png'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/scheduler_data.xml',
    ],

    'price': 1100,
    'currency': 'USD',
    'license': 'LGPL-3',
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'uninstall_hook': "uninstall_hook",
}
