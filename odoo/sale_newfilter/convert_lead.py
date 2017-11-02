from openerp.osv import fields, osv
from openerp.tools.translate import _
import re
import logging
_logger = logging.getLogger(__name__)

class ConvertToOppo(osv.osv_memory):
	_inherit='crm.lead2opportunity.partner'

	def default_get(self, cr, uid, fields, context=None):
		"""
		Default get for name, opportunity_ids.
		If there is an exisitng partner link to the lead, find all existing
		opportunities links with this partner to merge all information together
		"""
		lead_obj = self.pool.get('crm.lead')
		_logger.info('aaaaaaaaaaaaaaaaaaaaaaaaaaaaO MY GOD!!!!!!! %s',fields)
		res = super(ConvertToOppo, self).default_get(cr, uid, fields, context=context)
		_logger.info('000000000000000000000000000 MY GOD!!!!!!! %s',fields)
		if context.get('active_id'):
			#tomerge = [int(context['active_id'])]

			partner_id = res.get('partner_id')
			lead = lead_obj.browse(cr, uid, int(context['active_id']), context=context)
			email = lead.partner_id and lead.partner_id.email or lead.email_from

			# tomerge.extend(self._get_duplicated_leads(cr, uid, partner_id, email, include_lost=True, context=context))
			# tomerge = list(set(tomerge))

			if 'action' in fields and not res.get('action'):
				res.update({'action' : partner_id and 'exist' or 'create'})
			if 'partner_id' in fields:
				res.update({'partner_id' : partner_id})
			# if 'name' in fields:
			# 	res.update({'name' : len(tomerge) >= 2 and 'merge' or 'convert'})
			# if 'opportunity_ids' in fields and len(tomerge) >= 2:
			# 	res.update({'opportunity_ids': tomerge})
			if lead.user_id:
				res.update({'user_id': lead.user_id.id})
			if lead.section_id:
				res.update({'section_id': lead.section_id.id})
				
		return res

	def action_apply(self, cr, uid, ids, context=None):
		"""
		Convert lead to opportunity or merge lead and opportunity and open
		the freshly created opportunity view.
		"""
		_logger.info('O MY GOD!!!!!!! %s')
		if context is None:
			context = {}

		lead_obj = self.pool['crm.lead']
		partner_obj = self.pool['res.partner']

		w = self.browse(cr, uid, ids, context=context)[0]
		opp_ids = [o.id for o in w.opportunity_ids]
		vals = {
			'section_id': w.section_id.id,
		}
		if w.partner_id:
			vals['partner_id'] = w.partner_id.id
		if w.name == 'merge':
			lead_id = lead_obj.merge_opportunity(cr, uid, opp_ids, context=context)
			lead_ids = [lead_id]
			lead = lead_obj.read(cr, uid, lead_id, ['type', 'user_id'], context=context)
			if lead['type'] == "lead":
				context = dict(context, active_ids=lead_ids)
				vals.update({'lead_ids': lead_ids, 'user_ids': [w.user_id.id]})
				self._convert_opportunity(cr, uid, ids, vals, context=context)
			elif not context.get('no_force_assignation') or not lead['user_id']:
				vals.update({'user_id': w.user_id.id})
				lead_obj.write(cr, uid, lead_id, vals, context=context)
		else:
			lead_ids = context.get('active_ids', [])
			vals.update({'lead_ids': lead_ids, 'user_ids': [w.user_id.id]})
			self._convert_opportunity(cr, uid, ids, vals, context=context)
			for lead in lead_obj.browse(cr, uid, lead_ids, context=context):
				if lead.partner_id and lead.partner_id.user_id != lead.user_id:
					partner_obj.write(cr, uid, [lead.partner_id.id], {'user_id': lead.user_id.id}, context=context)

		return self.pool.get('crm.lead').redirect_opportunity_view(cr, uid, lead_ids[0], context=context)