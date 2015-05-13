# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
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
from tests.util import in_directory, run_scenario


@in_directory(__file__, 'django', 'couves')
def test_django_agains_couves():
    'it always call @after.all hooks, even after exceptions'

    status, out = run_scenario()

    assert "Couves before all" in out
    assert "Couves after all" in out


@in_directory(__file__, 'django', 'couves')
def test_django_agains_couves_nohooks():
    """
    it only calls @before.all and @after.all hooks if there are features found
    """

    status, out = run_scenario(**{'--tags': 'nothingwillbefound'})

    assert "Couves before all" not in out
    assert "Couves after all" not in out
