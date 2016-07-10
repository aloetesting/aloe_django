"""
Step definitions for working with Django email.
"""
from __future__ import print_function

from smtplib import SMTPException

from django.core import mail
from django.test.html import parse_html

from nose.tools import assert_in  # pylint:disable=no-name-in-module

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
    expected = int(count)
    actual = len(mail.outbox)
    assert expected == actual, \
        "Expected to send {0} email(s), got {1}.".format(expected, actual)


@step(r'I have not sent any emails')
def mail_not_sent(self):
    """
    Test no emails have been sent.

    Example:

    .. code-block:: gherkin

        Then I have not sent any emails
    """
    return mail_sent_count(self, 0)


@step(CHECK_PREFIX + (r'I have sent an email with "([^"]*)" in the ({0})')
      .format('|'.join(EMAIL_PARTS)))
def mail_sent_content(self, text, part):
    """
    Test an email contains (assert text in) the given text in the relevant
    message part (accessible as an attribute on the email object).

    This step strictly applies whitespace.

    Syntax:

        I have sent an email with "`text`" in the `part`

    Example:

    .. code-block:: gherkin

        Then I have sent an email with "pandas" in the body
    """
    if not any(text in getattr(email, part) for email in mail.outbox):
        dump_emails(part)
        raise AssertionError(
            "No email contained expected text in the {0}.".format(part))


@step(CHECK_PREFIX + (r'I have not sent an email with "([^"]*)" in the ({0})')
      .format('|'.join(EMAIL_PARTS)))
def mail_not_sent_content(self, text, part):
    """
    Test an email does not contain (assert text not in) the given text in the
    relevant message part (accessible as an attribute on the email object).

    This step strictly applies whitespace.

    Syntax:

        I have not sent an email with "`text`" in the `part`

    Example:

    .. code-block:: gherkin

        Then I have not sent an email with "pandas" in the body
    """
    if any(text in getattr(email, part) for email in mail.outbox):
        dump_emails(part)
        raise AssertionError(
            "An email contained unexpected text in the {0}.".format(part))


@step(CHECK_PREFIX + r'I have sent an email with the following in the body:')
def mail_sent_content_multiline(self):
    """
    Test the body of an email contains (assert text in) the given multiline
    string.

    This step strictly applies whitespace.

    Example:

    .. code-block:: gherkin

        Then I have sent an email with the following in the body:
        \"\"\"
        Dear Mr. Panda,
        \"\"\"
    """
    return mail_sent_content(self, self.multiline, 'body')


@step(CHECK_PREFIX +
      r'I have sent an email with the following HTML alternative:')
def mail_sent_contains_html(self):
    """
    Test that an email contains the HTML (assert HTML in) in the multiline as
    one of its MIME alternatives.

    The HTML is normalised by passing through Django's
    :func:`django.test.html.parse_html`.

    Example:

    .. code-block:: gherkin

        And I have sent an email with the following HTML alternative:
        \"\"\"
        <p><strong>Name:</strong> Sir Panda</p>
        <p><strong>Phone:</strong> 0400000000</p>
        <p><strong>Email:</strong> sir.panda@pand.as</p>
        \"\"\"
    """

    for email in mail.outbox:
        try:
            html = next(content for content, mime in email.alternatives
                        if mime == 'text/html')
            dom1 = parse_html(html)
            dom2 = parse_html(self.multiline)

            assert_in(dom1, dom2)

        except AssertionError as exc:
            print("Email did not match", exc)
            # we intentionally eat the exception
            continue

        return True

    raise AssertionError("No email contained the HTML")


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


def dump_emails(part):
    """Show the sent emails' tested parts, to aid in debugging."""

    print("Sent emails:")
    for email in mail.outbox:
        print(getattr(email, part))
