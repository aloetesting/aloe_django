# -*- coding: utf-8 -*-
"""
Test the harvest command.
"""

from nose.tools import (assert_equals,  # pylint:disable=no-name-in-module
                        assert_in,
                        assert_not_in)
from tests.util import in_directory, run_scenario


@in_directory(__file__, 'django', 'alfaces')
def test_django_agains_alfaces():
    """running the "harvest" django command with verbosity 3"""

    status, out = run_scenario()
    assert_equals(status, 0, out)

    assert_in("Test the django app DO NOTHING", out)
    assert_in("Test the django app FOO BAR", out)


@in_directory(__file__, 'django', 'alfaces')
def test_running_only_specified_features():
    """it can run only the specified features, passing the file path"""

    status, out = run_scenario('foobar', 'foobar')

    assert_equals(status, 0, out)

    assert_in("Test the django app FOO BAR", out)
    assert_not_in("Test the django app DO NOTHING", out)


@in_directory(__file__, 'django', 'alfaces')
def test_specifying_features_in_inner_directory():
    """it can run only the specified features from a subdirectory"""

    status, out = run_scenario('foobar', 'deeper/deeper/leaf')

    assert_equals(status, 0, out)

    assert_not_in("Test the django app FOO BAR", out)
    assert_in("Test a feature in an inner directory", out)
    assert_not_in("Test the django app DO NOTHING", out)


@in_directory(__file__, 'django', 'kale')
def test_run_with_tags():
    """it will only run specified tags"""

    status, out = run_scenario(attr='!fails')

    assert_equals(status, 0, out)
    assert_in("Ran 2 tests", out)


@in_directory(__file__, 'django', 'kale')
def test_run_with_tags_and_features():
    """it will only run specified tags in the feature files"""

    status, out = run_scenario('donothing', attr='!passes,!fails')

    assert_equals(status, 0, out)
    assert_in("Ran 1 test", out)
