# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _, _lt

_merchandise_export_code = {
    'BE': '29',
    'FR': '21'
}

_merchandise_import_code = {
    'BE': '19',
    'FR': '11'
}

class IntrastatReport(models.AbstractModel):
    _inherit = 'account.intrastat.report'


    @api.model
    def _build_query(self, date_from, date_to, journal_ids, invoice_types=None, with_vat=False):
        # triangular use cases are handled by letting the intrastat_country_id editable on
        # invoices. Modifying or emptying it allow to alter the intrastat declaration
        # accordingly to specs (https://www.nbb.be/doc/dq/f_pdf_ex/intra2017fr.pdf (§ 4.x))
        select = '''
                row_number() over () AS sequence,
                CASE WHEN inv.type IN ('in_invoice', 'out_refund') THEN %(import_merchandise_code)s ELSE %(export_merchandise_code)s END AS system,
                country.code AS country_code,
                company_country.code AS comp_country_code,
                CASE WHEN inv_line.intrastat_transaction_id IS NULL THEN '1' ELSE transaction.code END AS transaction_code,
                company_region.code AS region_code,
                code.code AS commodity_code,
                inv_line.id AS id,
                prodt.id AS template_id,
                inv.id AS invoice_id,
                inv.currency_id AS invoice_currency_id,
                inv.name AS invoice_number,
                coalesce(inv.invoice_date) AS invoice_date,
                inv.type AS invoice_type,
                inv_incoterm.code AS invoice_incoterm,
                comp_incoterm.code AS company_incoterm,
                inv_transport.code AS invoice_transport,
                comp_transport.code AS company_transport,
                CASE WHEN inv_line.intrastat_transaction_id IS NULL THEN '1' ELSE transaction.code END AS trans_code,
                CASE WHEN inv.type IN ('in_invoice', 'out_refund') THEN 'Arrival' ELSE 'Dispatch' END AS type,
                prod.weight * inv_line.quantity * (
                    CASE WHEN inv_line_uom.category_id IS NULL OR inv_line_uom.category_id = prod_uom.category_id
                    THEN 1 ELSE inv_line_uom.factor END
                ) AS weight,
                inv_line.quantity * (
                    CASE WHEN inv_line_uom.category_id IS NULL OR inv_line_uom.category_id = prod_uom.category_id
                    THEN 1 ELSE inv_line_uom.factor END
                ) AS quantity,
                inv_line.price_subtotal AS value
                '''
        from_ = '''
                account_move_line inv_line
                LEFT JOIN account_move inv ON inv_line.move_id = inv.id
                LEFT JOIN account_intrastat_code transaction ON inv_line.intrastat_transaction_id = transaction.id
                LEFT JOIN res_company company ON inv.company_id = company.id
                LEFT JOIN account_intrastat_code company_region ON company.intrastat_region_id = company_region.id
                LEFT JOIN res_partner partner ON inv_line.partner_id = partner.id
                LEFT JOIN res_partner comp_partner ON company.partner_id = comp_partner.id
                LEFT JOIN res_country country ON inv.intrastat_country_id = country.id
                LEFT JOIN res_country company_country ON comp_partner.country_id = company_country.id
                INNER JOIN product_product prod ON inv_line.product_id = prod.id
                LEFT JOIN product_template prodt ON prod.product_tmpl_id = prodt.id
                LEFT JOIN account_intrastat_code code ON prodt.intrastat_id = code.id
                LEFT JOIN uom_uom inv_line_uom ON inv_line.product_uom_id = inv_line_uom.id
                LEFT JOIN uom_uom prod_uom ON prodt.uom_id = prod_uom.id
                LEFT JOIN account_incoterms inv_incoterm ON inv.invoice_incoterm_id = inv_incoterm.id
                LEFT JOIN account_incoterms comp_incoterm ON company.incoterm_id = comp_incoterm.id
                LEFT JOIN account_intrastat_code inv_transport ON inv.intrastat_transport_mode_id = inv_transport.id
                LEFT JOIN account_intrastat_code comp_transport ON company.intrastat_transport_mode_id = comp_transport.id
                '''
        where = '''
                inv.state = 'posted'
                AND inv_line.display_type IS NULL
                AND NOT inv_line.quantity = 0
                AND inv.company_id = %(company_id)s
                AND company_country.id != country.id
                AND country.intrastat = TRUE
                AND coalesce(inv.date, inv.invoice_date) >= %(date_from)s
                AND coalesce(inv.date, inv.invoice_date) <= %(date_to)s
                AND prodt.type != 'service'
                AND inv.journal_id IN %(journal_ids)s
                AND inv.type IN %(invoice_types)s
                AND NOT inv_line.exclude_from_invoice_tab
                '''
        order = 'inv.invoice_date DESC'
        params = {
            'company_id': self.env.company.id,
            'import_merchandise_code': _merchandise_import_code.get(self.env.company.country_id.code, '29'),
            'export_merchandise_code': _merchandise_export_code.get(self.env.company.country_id.code, '19'),
            'date_from': date_from,
            'date_to': date_to,
            'journal_ids': tuple(journal_ids),
        }
        if with_vat:
            where += ' AND partner.vat IS NOT NULL '
        if invoice_types:
            params['invoice_types'] = tuple(invoice_types)
        else:
            params['invoice_types'] = ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')
        query = {
            'select': select,
            'from': from_,
            'where': where,
            'order': order,
        }
        return query, params
