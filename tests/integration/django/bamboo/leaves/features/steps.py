#

"""
Extra steps to test django mail steps
"""

from __future__ import print_function

import yaml

from django.core import mail

from aloe import step
from aloe_django.steps.mail import *


STEP_PREFIX = r'(?:Given|And|Then|When) '


def mail_send(data):
    html = data.pop('html', None)

    email = mail.EmailMultiAlternatives(**data)

    if html:
        email.attach_alternative(html, 'text/html')

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
