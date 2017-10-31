import json
from openerp import models, fields, api, _
import logging
from datetime import datetime, timedelta
from babel.dates import format_datetime, format_date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
_logger = logging.getLogger(__name__)

class MrpGraphKanban(models.Model):
	_name = "mrp.graph.kanban"

	def _kanban_dashboard_graph(self):
		return [{"values": [
					  {"value": 584.0, "label": "Anteriores"},
					  {"value": 739.73, "label": "29 feb-6 mar"},
					  {"value": 506.12, "label": "Esta semana"},
					  {"value": 233.6, "label": "14-20 mar"},
					  {"value": 0.0, "label": "21-27 mar"},
					  {"value": 0.0, "label": "Futuras"}
					], "id": self.id}]
	@api.one
	def _kanban_dashboard(self):
		self.kanban_dashboard_graph = json.dumps(self.get_bar_graph_datas())

	name = fields.Char("Name")
	kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard')

	@api.multi
	def action_create_new(self):
		ctx = self._context.copy()
		model = 'mrp.production.workcenter.line'
		view_id = self.env.ref('mrp_operations.mrp_production_workcenter_form_view_inherit').id
		return {
			'name': _('Work Order'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': model,
			'view_id': view_id,
			'context': ctx,
		}

	@api.multi
	def get_bar_graph_datas(self):
		data = []
		today = datetime.strptime(fields.Date.context_today(self), DF)
		data.append({'label': _('Previous'), 'value':0.0, 'type': 'past'})
		day_of_week = int(format_datetime(today, 'e', locale=self._context.get('lang', 'en_US')))
		first_day_of_week = today + timedelta(days=-day_of_week+1)
		for i in range(-1,4):
			if i==0:
				label = _('Current')
			elif i==3:
				label = _('Future')
			else:
				start_week = first_day_of_week + timedelta(days=i*7)
				end_week = start_week + timedelta(days=6)
				if start_week.month == end_week.month:
					label = str(start_week.day) + '-' +str(end_week.day)+ ' ' + format_date(end_week, 'MMM', locale=self._context.get('lang', 'en_US'))
				else:
					label = format_date(start_week, 'd MMM', locale=self._context.get('lang', 'en_US'))+'-'+format_date(end_week, 'd MMM', locale=self._context.get('lang', 'en_US'))
			data.append({'label':label,'value':0.0, 'type': 'past' if i<0 else 'future'})
		select_sql_clause = """SELECT sum(qty) as total, min(date_planned) as aggr_date from mrp_production_workcenter_line where state IN ('draft','startworking')"""
		query = ''
		start_date = (first_day_of_week + timedelta(days=-7))
		for i in range(0,6):
			if i == 0:
				query += "("+select_sql_clause+" and date_planned < '"+start_date.strftime(DF)+"')"
			elif i == 6:
				query += " UNION ALL ("+select_sql_clause+" and date_planned >= '"+start_date.strftime(DF)+"')"
			else:
				next_date = start_date + timedelta(days=7)
				query += " UNION ALL ("+select_sql_clause+" and date_planned >= '"+start_date.strftime(DF)+"' and date_planned < '"+next_date.strftime(DF)+"')"
				start_date = next_date
		self.env.cr.execute(query)
		query_results = self.env.cr.dictfetchall()
		for index in range(0, len(query_results)):
			if query_results[index].get('aggr_date') != None:
				data[index]['value'] = query_results[index].get('total')
		return [{'values': data, 'id': self.id}]