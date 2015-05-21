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
