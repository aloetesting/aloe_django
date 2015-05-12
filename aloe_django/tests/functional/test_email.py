import os
import sys
import commands

from nose.tools import assert_not_equals

from tests.util import in_directory


@in_directory(__file__)
def test_email():
    'Aloe should be able to receive emails sent from django server'

    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoapp'

        status, out = commands.getstatusoutput(
            "django-admin.py harvest email.feature --verbosity=2")

        assert_not_equals(status, 0)

    finally:
        del os.environ['DJANGO_SETTINGS_MODULE']
