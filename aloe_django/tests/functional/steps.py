from aloe import world, step
from aloe_django import mail

from nose.tools import assert_equals


@step(u'I visit "([^"]*)"')
def visit(step, url):
    # TODO: Make this a property of the step
    testclass = step.testclass
    base_url = testclass.live_server_url.__get__(testclass)
    url = urljoin(base_url, url)
    world.browser.visit(url)


@step(u'I see "([^"]*)"')
def see(step, text):
    assert world.browser.is_text_present(text)


@step(u'an email is sent to "([^"]*?)" with subject "([^"]*)"')
def email_sent(step, to, subject):
    message = mail.queue.get(True, timeout=5)
    assert_equals(message.subject, subject)
    assert_equals(message.recipients(), [to])
