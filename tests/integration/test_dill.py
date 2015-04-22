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
import commands
from nose.tools import assert_equals, assert_not_equals
from tests.util import in_directory, run_scenario



@in_directory(__file__, 'django', 'dill')
def test_model_creation():
    'Models are created through Lettuce steps'

    status, out = run_scenario('leaves', 'create')
    assert_equals(status, 0, out)


@in_directory(__file__, 'django', 'dill')
def test_model_update():
    'Models are updated through Lettuce steps'

    status, out = run_scenario('leaves', 'update', 1)
    assert_equals(status, 0, out)

    status, out = run_scenario('leaves', 'update', 2)
    assert_not_equals(status, 0, out)
    assert "IntegrityError" in out

    status, out = run_scenario('leaves', 'update', 3)
    assert_not_equals(status, 0, out)
    assert "The \"pk\" field is required for all update operations" in out

    status, out = run_scenario('leaves', 'update', 4)
    assert_not_equals(status, 0, out)
    assert "Must use the writes_models decorator to update models" in out


@in_directory(__file__, 'django', 'dill')
def test_model_existence_check():
    'Model existence is checked through Lettuce steps'

    status, out = run_scenario('leaves', 'existence', 1)
    assert_equals(status, 0, out)

    status, out = run_scenario('leaves', 'existence', 2)
    assert_not_equals(status, 0)
    assert "Garden does not exist: {u'name': u'Botanic Gardens'}" in out
    gardens = "\n".join([
        "Rows in DB are:",
        "id=1, name=Secret Garden, area=45, raining=False,",
        "id=2, name=Octopus's Garden, area=120, raining=True,",
        "id=3, name=Covent Garden, area=200, raining=True,",
    ])
    assert gardens in out
    assert "AssertionError: 1 rows missing" in out

    status, out = run_scenario('leaves', 'existence', 3)
    assert_not_equals(status, 0)
    assert "Garden does not exist: {u'name': u'Secret Garden', " \
        "u'@howbig': u'huge'}" in out
    gardens = "\n".join([
        "Rows in DB are:",
        "id=1, name=Secret Garden, area=45, raining=False, howbig=small,",
        "id=2, name=Octopus's Garden, area=120, raining=True, howbig=medium,",
        "id=3, name=Covent Garden, area=200, raining=True, howbig=big,",
    ])
    assert gardens in out
    assert "AssertionError: 1 rows missing" in out

    status, out = run_scenario('leaves', 'existence', 4)
    assert_not_equals(status, 0)
    assert "Expected 2 geese, found 1" in out

    status, out = run_scenario('leaves', 'existence', 5)
    assert_not_equals(status, 0)
    assert "Garden exists: {u'name': u'Secret Garden', " \
        "u'@howbig': u'small'}" in out
    assert "AssertionError: 1 rows found" in out
    gardens = "\n".join([
        "Rows in DB are:",
        "id=1, name=Secret Garden, area=45, raining=False, howbig=small,",
        "id=2, name=Octopus's Garden, area=120, raining=True, howbig=medium,",
        "id=3, name=Covent Garden, area=200, raining=True, howbig=big,",
    ])
    assert gardens in out


@in_directory(__file__, 'django', 'dill')
def test_use_test_database_setting():
    'Test database is recreated each time if LETTUCE_USE_TEST_DATABASE is set'

    for i in range(1, 2):
        status, out = commands.getstatusoutput(
            "python manage.py harvest --settings=testdbsettings -v 2 " +
            "leaves/features/testdb.feature")

        assert_equals(status, 0, out)
        assert "Harvester count: 1" in out, out
