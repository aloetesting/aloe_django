# -*- coding: utf-8 -*-
"""
Test mail steps.
"""

from tests.util import in_directory, run_scenario

from nose.tools import (  # pylint:disable=no-name-in-module
    assert_equals,
    assert_in,
    assert_not_equals,
)


@in_directory(__file__, 'django', 'bamboo')
def test_mail_count():
    'Mail count is checked through Lettuce steps'

    status, out = run_scenario('leaves', 'count', 1)
    assert_equals(status, 0, out)
    status, out = run_scenario('leaves', 'count', 2)
    assert_equals(status, 0, out)

    status, out = run_scenario('leaves', 'count', 3)
    assert_not_equals(status, 0)
    assert_in("Length of outbox is 1", out)


@in_directory(__file__, 'django', 'bamboo')
def test_mail_content():
    'Mail content is checked through Lettuce steps'

    status, out = run_scenario('leaves', 'content', 1)
    assert_equals(status, 0, out)
    status, out = run_scenario('leaves', 'content', 2)
    assert_equals(status, 0, out)
    status, out = run_scenario('leaves', 'content', 3)
    assert_equals(status, 0, out)

    status, out = run_scenario('leaves', 'content', 4)
    assert_not_equals(status, 0)
    assert_in("No email contained expected text in the body", out)

    status, out = run_scenario('leaves', 'content', 5)
    assert_not_equals(status, 0)
    assert_in("An email contained unexpected text in the body", out)

    status, out = run_scenario('leaves', 'content', 6)
    assert_not_equals(status, 0)
    assert_in("No email contained the HTML", out)


@in_directory(__file__, 'django', 'bamboo')
def test_mail_fail():
    'Mock mail failure dies with error'

    status, out = run_scenario('leaves', 'mock-failure', 1)
    assert_not_equals(status, 0)
    assert_in("SMTPException: Failure mocked by aloe", out)
