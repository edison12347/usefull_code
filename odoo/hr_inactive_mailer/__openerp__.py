# -*- coding: utf-8 -*-
##############################################################################
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
    'name': 'Inactive Employee Notification',
    'version': '2.0.1.0.0',
    'summary': """Send email notification when user become inactive""",
    'description': 'This module helps you to send email notification when user become inactive',
    'category': 'HR',
    'author': 'Ed Chu',
    'company': 'QArea',
    'depends': ['base', 'hr', 'email_template','contacts'],
    'data': ['views/hr_inactive_mailer.xml'
    ],
    'license': 'LGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
