from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class OdooExampleResPartner(models.Model):
    _inherit = 'res.partner'

    lead_count = fields.Integer(compute='_lead_count', string='Leads')
    opportunity_count = fields.Integer(compute='_opportunity_count', string='Opportunities', search="_search_opportunity")

    @api.one
    def _lead_count(self):
        partner_ids = self.env['crm.lead'].search([('partner_id', '=', self.id), ('type', '=', 'lead')])
        self.lead_count = len(partner_ids)

    @api.one
    def _opportunity_count(self):
        opportunity_ids = self.env['crm.lead'].search([('partner_id', '=', self.id), ('type', '=', 'opportunity')])
        self.opportunity_count = len(opportunity_ids)

    def _search_opportunity(self, operator, value):
        opps_ids = self.env['crm.lead'].search([('type', '=', 'opportunity')])
        partner_ids = list(set([opportunity.partner_id.id for opportunity in opps_ids]))
        return [('id', 'in', partner_ids)]