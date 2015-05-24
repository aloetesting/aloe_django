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

import os
import sys

from nose.tools import assert_not_equals

from tests.util import getstatusoutput, in_directory


@in_directory(__file__)
def test_email():
    'Aloe should be able to receive emails sent from django server'

    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoapp'

        status, out = getstatusoutput(
            "django-admin.py harvest email.feature --verbosity=2")

        assert_not_equals(status, 0)

    finally:
        del os.environ['DJANGO_SETTINGS_MODULE']
