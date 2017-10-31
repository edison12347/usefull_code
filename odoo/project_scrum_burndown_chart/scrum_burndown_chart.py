# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
import openerp.tools
import time
import json
from datetime import date, datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class burndownChart(models.Model):
    _inherit = 'project.scrum.sprint'
    _description = 'Project Scrum Burndown Chart'


    def _kanban_dashboard_graph(self):
        return [{"values": [
            {"value": 584.0, "label": "Anteriores"},
            {"value": 739.73, "label": "29 feb-6 mar"},
            {"value": 506.12, "label": "Esta semana"},
            {"value": 233.6, "label": "14-20 mar"},
            {"value": 0.0, "label": "21-27 mar"},
            {"value": 0.0, "label": "Futuras"}
        ], "id": self.id}]

    def get_task_effective_hours_on_date(self, task_works, current_day):
        task_hours_on_date = 0
        for task_work in task_works:
            day = datetime.strptime(task_work.date, '%Y-%m-%d %H:%M:%S')
            if current_day.date() == day.date():
                task_hours_on_date += task_work.hours
        _logger.info('gggggggggggggggg______task_hours_on_date________ggggggggggggg %s', task_hours_on_date)
        return task_hours_on_date



    def get_reamaning_work(self):

        chartData = [{"values": [], "id": self.id}]

        for sprint in self:
            total_effective_work = 0
            remaning_work = 0
            try:

                dateStart = datetime.strptime(sprint.date_start, '%Y-%m-%d')
                dateStop = datetime.strptime(sprint.date_stop, '%Y-%m-%d')
                no_of_days = dateStop.date() - dateStart.date()
            except TypeError:
                _logger.warning('---------> Sprint dates are not valid!, check sprint number %s, called %s', sprint.id, sprint.name)
            else:
                sprint_task = self.env['project.task'].search([('sprint_id', '=', sprint.id)])
                for day in range(no_of_days.days + 1):
                    daily_effective_hours = 0
                    current_day = dateStart + timedelta(days=day)
                    for task in sprint_task:
                        daily_effective_hours += self.get_task_effective_hours_on_date(task.work_ids, current_day)
                    total_effective_work += daily_effective_hours
                    remaning_work = sprint.planned_hours - total_effective_work
                    if daily_effective_hours > 0 or day == 0:
                        chartData[0]["values"].append({"value": remaning_work, "label": str(current_day.date())})
                    else:
                        chartData[0]["values"].append({"value": 0, "label": str(current_day.date())})

        _logger.info('gggggggggggggggg______chartData_________ggggggggggggg %s', chartData)
        return chartData




    @api.one
    def _kanban_dashboard(self):
        self.get_reamaning_work()
        self.kanban_burndown_chart = json.dumps(self.get_reamaning_work())

    kanban_burndown_chart = fields.Text(compute='_kanban_dashboard')