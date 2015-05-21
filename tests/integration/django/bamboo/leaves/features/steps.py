# Aloe-Django - Package for testing Django applications with Aloe
# Copyright (C) <2015> Alexey Kotlyarov <a@koterpillar.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Extra steps to test django mail steps
"""

import yaml

from django.core import mail

from aloe import step
from aloe_django.steps.mail import *


STEP_PREFIX = r'(?:Given|And|Then|When) '


def mail_send(data):
    email = mail.EmailMessage(**data)
    email.send()


@step(r'I send a test email$')
def mail_send_simple(step):
    """
    Send a test, predefined email
    """
    mail_send({
        'from_email': 'test-no-reply@infoxchange.net.au',
        'to': ['other-test-no-reply@infoxchange.au'],
        'subject': 'Lettuce Test',
        'body': 'This is a test email sent from aloe, right to your door!',
    })


# send email with yaml
@step(r'I send a test email with the following set:$')
def mail_send_yaml(step):
    """
    Send a test email from loaded yaml
    """

    mail_send(yaml.load(step.multiline))
