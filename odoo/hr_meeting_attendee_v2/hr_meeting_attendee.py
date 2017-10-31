from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class meeting_attendee(models.Model):

    """ Model for Calendar Event """
    _name = 'calendar.event'
    _inherit = 'calendar.event'
    _description = "Parse and adds attendees to the partner_ids in meetings"

    def create(self, cr, uid, vals, context=None):

        if context is None:
            context = {}

        self._set_date(cr, uid, vals, id=False, context=context)
        if not 'user_id' in vals:  # Else bug with quick_create when we are filter on an other user
            vals['user_id'] = uid
            
        applicant_id = context.get('active_id',False)
        application = self.pool.get('hr.applicant').browse(cr, uid, applicant_id)
        application_creator = application.create_uid
        application_creator_id = application_creator.partner_id.id
        job = application.job_id
        job_creator = job.create_uid
        job_creator_id = job_creator.partner_id.id
        res = super(meeting_attendee, self).create(cr, uid, vals, context=context)
        if (application_creator_id or job_creator_id) is not False:
        # add aplicant and job creators to the list
            partner_ids_list = []
            partner_ids_list.append([4, application_creator_id])
            partner_ids_list.append([4, job_creator_id])
            vals['partner_ids'] = partner_ids_list
            res = super(meeting_attendee, self).create(cr, uid, vals, context=context)
            final_date = self._get_recurrency_end_date(cr, uid, res, context=context)
            self.write(cr, uid, [res], {'final_date': final_date}, context=context)
            self.create_attendees(cr, uid, [res], context=context)

        return res