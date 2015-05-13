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


@in_directory(__file__, 'django', 'celeries')
def test_failfast():
    'passing --failfast to the harvest command will cause aloe to stop in the first failure'

    status, output = run_scenario(**{'--failfast': None})

    assert "This one is present" in output
    assert "Celeries before all" in output
    assert "Celeries before harvest" in output
    assert "Celeries before feature 'Test the django app leaves'" in output
    assert "Celeries before scenario 'This one is present'" in output

    assert "Celeries before step 'Given I say foo bar'" in output
    assert "Celeries after step 'Given I say foo bar'" in output
    assert "Celeries before step 'Then it fails'" in output
    assert "Celeries after step 'Then it fails'" in output

    assert "Celeries after scenario 'This one is present'" in output
    assert "Celeries after feature 'Test the django app leaves'" in output
    assert "Celeries after harvest" in output
    assert "Celeries after all" in output

    assert "This one is never called" not in output
