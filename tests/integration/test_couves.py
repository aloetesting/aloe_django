# -*- coding: utf-8 -*-
# Aloe-Django - Package for testing Django applications with Aloe
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
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

from nose.tools import (
    assert_in,
    assert_not_in,
)

from tests.util import in_directory, run_scenario


@in_directory(__file__, 'django', 'couves')
def test_django_agains_couves():
    'it always call @after.all hooks, even after exceptions'

    status, out = run_scenario(**{'-s': None})

    assert_in("Couves before all", out)
    assert_in("Couves after all", out)


@in_directory(__file__, 'django', 'couves')
def test_django_agains_couves_nohooks():
    """
    it only calls @before.all and @after.all hooks if there are features found
    """

    status, out = run_scenario(**{
        '--tags': 'nothingwillbefound',
        '-s': None,
    })

    assert_not_in("Couves before all", out)
    assert_not_in("Couves after all", out)
