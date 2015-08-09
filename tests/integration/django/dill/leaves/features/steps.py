#

import io
import json
import sys

from django.core.management import call_command

from leaves.models import (
    Harvester,
    Panda,
)

from aloe import after, step
from aloe.tools import guess_types
from aloe_django.steps.models import (
    test_existence,
    tests_existence,
    write_models,
    writes_models,
)

from nose.tools import assert_equals

max_rego = 0


@writes_models(Harvester)
def write_with_rego(data, field=None):
    for hash_ in data:
        hash_['rego'] = hash_['make'][:3].upper() + "001"

    write_models(Harvester, data, field=field)


@tests_existence(Harvester)
def check_with_rego(queryset, data):
    try:
        data['rego'] = data['rego'].upper()
    except KeyError:
        pass
    return test_existence(queryset, data)


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


@writes_models(Panda)
def write_pandas(data, field):
    # It is not necessary to call hashes_data/guess_types, but it might be
    # present in old code using the library. Test that it is a no-op
    # in that case.
    data = guess_types(data)

    for hash_ in data:
        if 'name' in hash_:
            hash_['name'] += ' Panda'

    return write_models(Panda, data, field)
