# -*- coding: utf-8 -*-
#

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
