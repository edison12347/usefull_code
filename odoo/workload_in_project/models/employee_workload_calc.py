# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Jesni Banu(<http://www.cybrosys.com>)
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
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, timedelta
from openerp import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)

DEF_WORK_DAYS = 5
DEF_NO_OF_DAYS = 7
DEF_WORK_HR = 8
TODAY = datetime.today().date()


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    current_workload = fields.Integer(string='Current Workload', default=0)
    maximum_rate = fields.Integer(string='Maximum rate', default=100)
    users_workload_hrs = fields.Integer(string='Current Workload [hrs]')
    max_workload = fields.Integer(string='Maximum workload [hrs]')

    """
    Function takes calculates workload based on remaining time for all tasks within the deadline and maximum workload
    """

    def determine_workload_timeframe(self, no_of_days):
        if no_of_days:
            workload_boundary_date = datetime.today() + timedelta(days=no_of_days - 1)
        else:
            workload_boundary_date = datetime.today() + timedelta(days=DEF_NO_OF_DAYS)
            no_of_days = DEF_NO_OF_DAYS
        return (workload_boundary_date, no_of_days)

    def get_users_taskwork_hours(self, user, workload_boundary_date):
        query = "SELECT sum(abs(remaining_hours)) as users_workload_hrs from project_task WHERE " \
                "user_id = '" + str(user.id) + "'" + \
                " AND date_deadline >= '" + datetime.today().date().strftime(DF) + "'" + \
                " AND date_deadline <= '" + workload_boundary_date.date().strftime(DF) + "';"
        self.env.cr.execute(query)
        query_results = self.env.cr.fetchone()
        users_workload_hrs = 0 if query_results[0] is None else query_results[0]
        return users_workload_hrs

    def calc_max_workload_calendar_based(self, work_schedule, no_of_days):
        max_workload = 0.0

        hours_in_weekday = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
        work_time = work_schedule.attendance_ids

        # Write work schedule hours into dict
        for schedule_line in work_time:
            time = schedule_line.hour_to - schedule_line.hour_from
            hours_in_weekday[str(schedule_line.dayofweek)] += time

        # Calculate max_workload for a give period
        for day in range(no_of_days):
            current_day = TODAY + timedelta(days=day)
            max_workload += hours_in_weekday[str(current_day.weekday())]

        return (max_workload, hours_in_weekday)

    def calc_standard_max_workload(self, no_of_days, no_of_hrs):
        max_workload = 0

        for day in range(no_of_days):
            current_day = TODAY + timedelta(days=day)
            if current_day.weekday() in range(DEF_WORK_DAYS):
                if no_of_hrs != 0 and no_of_hrs != None:
                    max_workload += no_of_hrs
                else:
                    max_workload += DEF_WORK_HR
        return max_workload

    def calc_leaves_queary(self, user, workload_boundary_date):  # NOT USED
        # TODO calculation can be improved by using direct query for leaves

        leaves_time_query = "SELECT sum(abs(remaining_hours)) as users_workload_hrs from project_task WHERE " \
                            "user_id = '" + str(user.id) + "'" + \
                            " AND date_deadline >= '" + datetime.today().date().strftime(DF) + "'" + \
                            " AND date_deadline <= '" + workload_boundary_date.date().strftime(DF) + "';"
        self.env.cr.execute(leaves_time_query)
        leaves_time = self.env.cr.fetchone()
        return leaves_time

    def calc_workload_after_leaves(self, work_schedule, max_workload_before_leaves,
                                   workload_boundary_date, hours_in_weekday):
        # Substract leaves from max_workload for a given period
        max_workload_after_leaves = max_workload_before_leaves
        leaves = work_schedule.leave_ids
        for leave in leaves:
            date_to = datetime.strptime(leave.date_to, '%Y-%m-%d %H:%M:%S')
            date_from = datetime.strptime(leave.date_from, '%Y-%m-%d %H:%M:%S')
            diff = date_to - date_from
            if date_from >= datetime.today():
                for day in range(diff.days + 1):  # if there is a leave it is at least one day
                    current_day = date_from + timedelta(days=day)
                    if current_day < workload_boundary_date:
                        max_workload_after_leaves -= hours_in_weekday[str(current_day.weekday())]
                        return (max_workload_after_leaves, hours_in_weekday)
                    else:
                        break

    def udate_workload(self, user, workload):
        query = "UPDATE res_users SET current_workload = '" + str(int(workload)) + "' WHERE id = '" + str(user.id) + "';" 
        self.env.cr.execute(query)

    @api.one
    def _calc_workload(self):
        ir_values = self.env['ir.values']
        no_of_days = ir_values.get_default('project.config.settings', 'no_of_days')
        no_of_hrs = ir_values.get_default('project.config.settings', 'working_hr')

        # Look at the each user and select task within deadlines
         if no_of_days == 0:
            self.udate_workload(self, 0)
        else:
            workload_boundary_date, no_of_days = self.determine_workload_timeframe(no_of_days)

        users_workload_hrs = self.get_users_taskwork_hours(self, workload_boundary_date)

        # Calculate users max load
        employee = self.env['hr.employee'].search([('id', '=', self.id)])
        if len(employee.calendar_id) != 0:  # If there is a schedule calculate max workload based on it
            work_schedule = employee.calendar_id
            max_workload, hours_in_weekday = self.calc_max_workload_calendar_based(work_schedule, no_of_days)
            max_workload, hours_in_weekday = self.calc_workload_after_leaves(work_schedule,
                                                                             max_workload,
                                                                             workload_boundary_date,
                                                                             hours_in_weekday)
        else:  # If there is no schedule use default values
            max_workload = self.calc_standard_max_workload(no_of_days, no_of_hrs)

        workload_perc = (users_workload_hrs / max_workload) * 100
        self.progress_rate = workload_perc
        self.current_workload = workload_perc
        self.udate_workload(self, workload_perc)
        self.users_workload_hrs = users_workload_hrs


    def _empty_function(self):
        pass

    def _search_free_user(self, operator, value):
        users_ids = self.env['res.users'].search([('current_workload', '=', 0)])
        users_list = list(set([user.id for user in users_ids]))
        return [('id', 'in', users_list)]

    def _search_overloaded_user(self, operator, value):
        users_ids = self.env['res.users'].search([('current_workload', '>', 100)])
        users_list = list(set([user.id for user in users_ids]))
        return [('id', 'in', users_list)]

    def _my_dep_filter(self, operator, value):
        current_user_employee_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        department_list = [employee.department_id.id for employee in current_user_employee_ids]
        current_departments_employee_ids = self.env['hr.employee'].search([('department_id', 'in', department_list)])
        user_list = [employee.user_id.id for employee in current_departments_employee_ids]
        return [('id', 'in', user_list)]

    progress_rate = fields.Integer(string='Workload', compute=_calc_workload)
    low_load = fields.Integer(string='Low Workload', compute=_empty_function, search="_search_free_user")
    overload = fields.Integer(string='Overload', compute=_empty_function, search="_search_overloaded_user")
    my_dep_filter = fields.Integer(string='Department filter', compute=_empty_function, search="_my_dep_filter")



class Project_workload(models.Model):
    _inherit = 'project.project'

    @api.multi
    def employee_project_filter(self):
        # TODO figure out how to add 'search_view_id', current one doesn't work
        members_list = list([user.id for user in self.members])
        employee_ids = self.env['hr.employee'].search([('user_id', 'in', members_list)])
        employee_list = list(set([employee.id for employee in employee_ids]))
        view_id_kanban = self.env['ir.model.data'].get_object_reference('workload_in_project', 'workload_kanban_view')
        view_id_tree = self.env['ir.model.data'].get_object_reference('workload_in_project', 'workload_tree_view')
        view_id_search = self.env['ir.model.data'].get_object_reference('workload_in_project', 'view_workload_filter')
        # _logger.info("+++++++++++++view_id_search++++++++++> %s", view_id_search)
        return {
            'name': _("Project Workload Filtered by Project"),
            'view_mode': "kanban, tree",
            'view_type': 'form',
            'res_model': 'res.users',
            'type': 'ir.actions.act_window',
            'search_view_id': view_id_search[1],
            'views': [(view_id_kanban[1], 'kanban'),(view_id_tree[1], 'tree')],
            'target': 'current',
            'domain': "[('id', 'in', {})]".format(employee_list),
        }


class ProjectSettings(models.TransientModel):
    _inherit = 'project.config.settings'

    working_hr = fields.Integer(string='Standard working Hr/day', default=DEF_WORK_HR)
    no_of_days = fields.Integer(string='No of days for calculation', default=DEF_NO_OF_DAYS)
    block_busy_users = fields.Boolean(string='Block busy users ?', default=False)

    @api.multi
    def set_block_busy_users(self):
        return self.env['ir.values'].sudo().set_default(
            'project.config.settings', 'block_busy_users', self.block_busy_users)

    @api.multi
    def set_working_hr(self):
        return self.env['ir.values'].sudo().set_default(
            'project.config.settings', 'working_hr', self.working_hr)

    @api.multi
    def set_no_of_days(self):
        return self.env['ir.values'].sudo().set_default(
            'project.config.settings', 'no_of_days', self.no_of_days)


class ProjectInherit(models.Model):
    _inherit = 'project.task'

    @api.constrains('user_id')
    def validation(self):
        ir_values = self.env['ir.values']
        block_users = ir_values.get_default('project.config.settings', 'block_busy_users')
        if block_users:
            if self.user_id.progress_rate > 80:
                raise Warning(
                    _('%s is %s percentage Overloaded with Work') % (self.user_id.name, self.user_id.progress_rate))


class EmployeeWorkloadReport(models.TransientModel):

    # TODO close wizard after downloading a report
    _name = "wizard.workload.report"
    _description = "Employee Workload Report"

    working_hr = fields.Integer(string='Working Hr/day', required=True, default=DEF_WORK_HR)
    from_date = fields.Date(string='From Date', required=True, default=lambda *a: datetime.now().strftime('%Y-%m-%d'))
    to_date = fields.Date(string='To Date', required=True, default=datetime.today() + timedelta(days=DEF_NO_OF_DAYS))

    @api.multi
    def workload_report(self):
        data = self.read()[0]
        datas = {
            'ids': [],
            'model': 'wizard.workload.report',
            'form': data
        }
        return self.env['report'].get_action(self, 'workload_in_project.report_employee_workload', data=datas)
