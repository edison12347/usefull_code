# -*- coding: utf-8 -*-
##############################################################################
#
#    Simbioz
#    Copyright (C) 2017-TODAY Simbioz(<http://www.baspar.eu>).
#    Author: Ed Chu(<http://www.baspar.eu>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from dateutil.relativedelta import relativedelta
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import fields, api, _
from openerp.http import request

import logging
_logger = logging.getLogger(__name__)

class EmployeeWorkloadReportCommon(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(EmployeeWorkloadReportCommon, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_line': self.get_lines,
        })
        self.context = context

    def get_lines(self, data):
        users = request.env['res.users'].search([])
        lines = []
        for user in users:
            tasks_within_period = request.env['project.task'].search([('user_id', '=', user.id),
                                                       ('date_deadline', '>=', data['form']['from_date']),
                                                       ('date_deadline', '<=', data['form']['to_date'])])

            workload_hrs = user.users_workload_hrs
            workload_perc = user.progress_rate

            if workload_perc > 100:
                status = 'Over Workload'
            elif workload_perc > 75:
                status = 'Busy'
            elif workload_perc > 50:
                status = 'Normal'
            elif workload_perc > 0:
                status = 'Less Workload'
            else:
                status = 'Free'
            vals = {
                'employee': user.name,
                'no_of_works': len(tasks_within_period),
                'workload': workload_hrs,
                'workload_perc': '{:.2f}'.format(workload_perc),
                'status': status,
            }
            lines.append(vals)
        return lines


class PrintReport(osv.AbstractModel):
    _name = 'report.workload_in_project.report_employee_workload'
    _inherit = 'report.abstract_report'
    _template = 'workload_in_project.report_employee_workload'
    _wrapped_report_class = EmployeeWorkloadReportCommon
