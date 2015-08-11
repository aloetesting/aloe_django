# -*- coding: utf-8 -*-
"""
Test hooks in harvest
"""

from nose.tools import (
    assert_in,
    assert_not_in,
)

from tests.util import in_directory, run_scenario


@in_directory(__file__, 'django', 'couves')
def test_django_agains_couves():
    'it always call @after.all hooks, even after exceptions'

    _, out = run_scenario(**{'-s': None})

    assert_in("Couves before all", out)
    assert_in("Couves after all", out)


@in_directory(__file__, 'django', 'couves')
def test_django_agains_couves_nohooks():
    """
    it only calls @before.all and @after.all hooks if there are features found
    """

    _, out = run_scenario(**{
        '--tags': 'nothingwillbefound',
        '-s': None,
    })

    assert_not_in("Couves before all", out)
    assert_not_in("Couves after all", out)
