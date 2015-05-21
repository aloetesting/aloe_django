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

import os
import time
import multiprocessing

from nose.tools import assert_equals, assert_not_equals
from tests.util import getstatusoutput, in_directory


@in_directory(__file__, 'django', 'alfaces')
def test_django_agains_alfaces():
    'running the "harvest" django command with verbosity 3'

    status, out = getstatusoutput(
        "python manage.py harvest --verbosity=3")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" in out
    assert "Test the django app FOO BAR" in out


@in_directory(__file__, 'django', 'alfaces')
def test_running_only_specified_features():
    'it can run only the specified features, passing the file path'

    status, out = getstatusoutput(
        "python manage.py harvest --verbosity=3 "
        "foobar/features/foobar.feature")

    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" in out
    assert "Test the django app DO NOTHING" not in out


@in_directory(__file__, 'django', 'alfaces')
def test_specifying_features_in_inner_directory():
    'it can run only the specified features from a subdirectory'

    status, out = getstatusoutput(
        "python manage.py harvest --verbosity=3 "
        "foobar/features/deeper/deeper/leaf.feature")

    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" not in out
    assert "Test a feature in an inner directory" in out
    assert "Test the django app DO NOTHING" not in out
