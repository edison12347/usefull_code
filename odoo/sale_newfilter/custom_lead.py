from openerp import fields, models, api, exceptions, osv


class CustomLead(models.Model):

	_inherit = 'crm.lead'

	section_id = fields.Many2one('crm.case.section', 'Sales Team',
                        select=True, track_visibility='onchange',
                        domain=[('type_team', '=', 'sale')],
                        help='When sending mails, the default email address is taken from the sales team.')
	crm_nda = fields.Boolean('NDA', default=False)
	user_id2 = fields.Many2one('res.users', 'External Sales Person')
	# lead_type = fields.Selection([('test', 'Test'),('sql', 'SQL'),
 #                                  ('sales_partners', 'Sales Partners'),
 #                                  ('marketing_partners', 'Marketing Partners'),
 #                                  ('qa_resources', 'QA Resources'),
 #                                  ('software_development_resources', 'Software Development Resources')],
 #                                 string='Type of the lead', default='sql')
	lead_type_ids = fields.Many2many('crm.lead.type', 'crm_lead_type_rel', 'lead_id', 'id', 'Type of the lead',)
	industry = fields.Selection([('fintech', 'Fintech & Banking'),
								('ecommerce', 'E-commerce & Retail'),
								('healthcare', 'Healthcare & Medicine'),
								('automotive', 'Automotive'),
								('media', 'Media & Entertainment'),
								('travel', 'Travel & Hospitality'),
								('education', 'Education'),
								('crm', 'CRM'),
								('navigation', 'Navigation'),
								('social_network', 'Social Networks')], string = 'Industry')

class crm_lead_type(models.Model):
	_name = 'crm.lead.type'

	name = fields.Char(string='Name')
	lead_id = fields.Many2one('crm.lead', string='Lead')