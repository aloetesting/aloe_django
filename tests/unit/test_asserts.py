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
