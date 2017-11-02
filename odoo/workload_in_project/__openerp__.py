# -*- coding: utf-8 -*-
##############################################################################
#
#    Simbioz Holding LLC
#    Copyright (C) 2016-TODAY Simbioz Holding LLC (<http://www.baspar.eu>).
#    Author: Author Name (<http://www.baspar.eu>)
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
{
    'name': 'Workload In Project',
    'version': '2.0.1.0.0',
    'summary': """Calculate The Workload For Employees In Project""",
    'description': 'This module helps you to calculate workload for employees',
    'category': 'Project',
    'author': 'Ed Chu',
    'company': 'Simbioz',
    'website': "http://www.baspar.eu/",
    'depends': ['base', 'project', 'hr_timesheet'],
    'data': [
        'views/employee_workload_report_view.xml',
        'reports/employee_workload_report.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
