# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import binascii
import tempfile

import xlrd

from odoo import models, fields, api


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    i_love_ddls = fields.Boolean('I Love Dedoles', default=True, store=True, readonly=False)
    employee_contacts = fields.Binary('Employee Contacts', attachment=False)
    employee_contacts_filename = fields.Char()
    salary = fields.Integer('Salery', required=True, default=0, store=True, readonly=False)
    tax = fields.Integer('Tax', required=True, default=0, store=True, readonly=False)
    total_salary = fields.Integer("Total Salary", compute="_compute_total_salary", store=False, readonly=True)

    @api.depends("salary", "tax")
    def _compute_total_salary(self):
        for record in self:
            record.total_salary = record.salary + record.tax

    def action_send_contacts_email(self):
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.employee_contacts))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        for row_no in range(sheet.nrows):
            row = sheet.row(row_no)

            vals = {
                'subject': row[1].value,
                'body_html': "Welcome in Dedoles",
                'email_to': row[0].value,
            }
            self.env['mail.mail'].sudo().create(vals).send()
        return


