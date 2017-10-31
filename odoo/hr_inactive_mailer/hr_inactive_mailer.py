# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Ed Chu 
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
from openerp import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class Inactive_mailer(models.Model):
    _inherit = 'hr.employee'

    @api.one
    # @api.depends('active')
    def _get_info4url(self):

        self.action_id = self.env.ref('hr.open_view_employee_list')
        self.url = self.env['base.config.settings'].get_default_alias_domain().get('alias_domain')
        self.admin_email = self.env['res.users'].search([('id', '=', '1')]).email
        return 0

    admin_email = fields.Char(string='Email')
    action_id = fields.Integer(string='Action')
    url = fields.Char(string='Domain')

    @api.multi
    def send_mail_template(self):

        template = self.env.ref('hr_inactive_mailer.inactive_employee_email_template')
        return self.env['email.template'].browse(template.id).send_mail(self.id)

    @api.multi
    def write(self, vals):
        if 'active' in vals and vals['active'] == False:
            self._get_info4url()
            self.send_mail_template()
        return super(Inactive_mailer, self).write(vals)




