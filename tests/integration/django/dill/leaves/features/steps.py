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

import io
import json
import sys

from django.core.management import call_command

from leaves.models import *

from aloe import after, step
from aloe_django.steps.models import *

from nose.tools import assert_equals

max_rego = 0


@creates_models(Harvester)
def create_with_rego(step):
    data = hashes_data(step)
    for hash_ in data:
        hash_['rego'] = hash_['make'][:3].upper() + "001"
    create_models(Harvester, data)


@tests_existence(Harvester)
def check_with_rego(data):
    try:
        data['rego'] = data['rego'].upper()
    except KeyError:
        pass
    return test_existence(Harvester, data)


@step(r'The database dump is as follows')
def database_dump(step):
    if sys.version_info >= (3, 0):
        output = io.StringIO()
    else:
        output = io.BytesIO()
    call_command('dumpdata', stdout=output, indent=2)
    output = output.getvalue()
    assert_equals(json.loads(output), json.loads(step.multiline))


@step(r'I have populated the database')
def database_populated(step):
    pass


@step(r'I count the harvesters')
def count_harvesters(step):
    print("Harvester count: %d" % Harvester.objects.count())


@creates_models(Panda)
def create_pandas(step):
    data = hashes_data(step)

    if 'name' in data:
        data['name'] += ' Panda'

    return create_models(Panda, data)
