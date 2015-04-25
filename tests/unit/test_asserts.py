"""
Test cases for the assertion tests
"""

from nose.tools import assert_equals

from tests import asserts


def test_yield_transitions():
    """
    Test yield_transitions
    """

    assert_equals(
        list(asserts.yield_transitions("1111112222221111")),
        [
            (0, 6, '1'),
            (6, 12, '2'),
            (12, 16, '1'),
        ]
    )
