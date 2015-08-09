#

"""
Step definitions for working with Django email.
"""
from smtplib import SMTPException

from django.core import mail

from aloe import step

__all__ = ()


STEP_PREFIX = r'(?:Given|And|Then|When) '
CHECK_PREFIX = r'(?:And|Then) '
EMAIL_PARTS = ('subject', 'body', 'from_email', 'to', 'bcc', 'cc')
GOOD_MAIL = mail.EmailMessage.send


@step(CHECK_PREFIX + r'I have sent (\d+) emails?')
def mail_sent_count(self, count):
    """
    Test that `count` mails have been sent.

    Syntax:

        I have sent `count` emails

    Example:

    .. code-block:: gherkin

        Then I have sent 2 emails
    """
    count = int(count)
    assert len(mail.outbox) == count, "Length of outbox is {0}".format(count)


@step(r'I have not sent any emails')
def mail_not_sent(self):
    """
    Test no emails have been sent.

    Example:

    .. code-block:: gherkin

        Then I have not sent any emails
    """
    return mail_sent_count(self, 0)


@step(CHECK_PREFIX + (r'I have sent an email with "([^"]*)" in the ({0})'
                      '').format('|'.join(EMAIL_PARTS)))
def mail_sent_content(self, text, part):
    """
    Test an email contains the given text in the relevant message part
    (accessible as an attribute on the email object).

    Syntax:

        I have sent an email with "`text`" in the `part`

    Example:

    .. code-block:: gherkin

        Then I have sent an email with "pandas" in the body
    """
    assert any(text in getattr(email, part)
               for email
               in mail.outbox), \
        "An email contained expected text in the {0}".format(part)


@step(CHECK_PREFIX + r'I have sent an email with the following in the body:')
def mail_sent_content_multiline(self):
    """
    Test the body of an email contains the given multiline string.

    This step strictly applies whitespace.

    Example:

    .. code-block:: gherkin

        Then I have sent an email with the following in the body:
        \"\"\"
        Dear Mr. Panda,
        \"\"\"
    """
    return mail_sent_content(self, self.multiline, 'body')


@step(STEP_PREFIX + r'I clear my email outbox')
def mail_clear(self):
    """
    Clear the email outbox.

    Example:

    .. code-block:: gherkin

        Given I clear my email outbox
    """
    mail.EmailMessage.send = GOOD_MAIL
    mail.outbox = []


def broken_send(*args, **kwargs):
    """
    Broken send function for email_broken step
    """
    raise SMTPException("Failure mocked by aloe_django")


@step(STEP_PREFIX + r'sending email does not work')
def email_broken(self):
    """
    Cause sending email to raise an exception.

    This allows simulating email failure.

    Example:

    .. code-block:: gherkin

        Given sending email does not work
    """
    mail.EmailMessage.send = broken_send
