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

"""
Step definitions for working with Django models.
"""

from __future__ import print_function
from builtins import bytes
from builtins import str

from datetime import datetime
import re
import warnings

from django.core.management import call_command
from django.core.management.color import no_style
from django.db import connection
from django.db.models.loading import get_models
from django.utils.functional import curry
from functools import partial, wraps

from aloe import step


STEP_PREFIX = r'(?:Given|And|Then|When) '


def _models_generator():
    """
    Build a hash of model verbose names to models
    """
    for model in get_models():
        yield (str(model._meta.verbose_name), model)
        yield (str(model._meta.verbose_name_plural), model)


MODELS = dict(_models_generator())


_WRITE_MODEL = {}


def creates_models(model):
    """
    Register a model-specific creation function. Wrapper around writes_models
    that removes the field parameter (always a create operation).
    """

    def decorated(func):

        @wraps(func)
        @writes_models(model)
        def wrapped(data, field):
            if field:
                raise NotImplementedError(
                    "Must use the writes_models decorator to update models")
            return func(data)

    return decorated


def writes_models(model):
    """
    Register a model-specific create and update function.

    The function must accept a list of data hashes and a field name. If field
    is not None, it is the field that must be used to get the existing objects
    out of the database to update them; otherwise, new objects must be created
    for each data hash.
    """

    def decorated(func):
        """
        Decorator for the creation function.
        """
        _WRITE_MODEL[model] = func
        return func

    return decorated


_MODEL_EXISTS = {}


def checks_existence(model):
    """
    Register a model-specific existence check function.

    This is deprecated, use tests_existence which checks individual hashes and
    can reuse diagnostic information from the generic existence check.
    """

    warnings.warn("deprecated - use tests_existence", DeprecationWarning)

    def decorated(func):
        """
        Decorator for the existence function.
        """
        _MODEL_EXISTS[model] = func
        return func

    return decorated


_TEST_MODEL = {}


def tests_existence(model):
    """
    Register a model-specific existence test.
    """

    def decorated(func):
        """
        Decorator for the existence function.
        """
        _TEST_MODEL[model] = func
        return func

    return decorated


def hash_data(hash_):
    """
    Convert strings from a step table to appropriate types.
    """
    res = {}
    for key, value in hash_.items():
        if isinstance(value, bytes):
            value = value.decode()
        if isinstance(value, str):
            if value == "true":
                value = True
            elif value == "false":
                value = False
            elif value == "null":
                value = None
            elif value.isdigit() and not re.match("^0[0-9]+", value):
                value = int(value)
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                value = datetime.strptime(value, "%Y-%m-%d")
        res[key] = value
    return res


def hashes_data(data):
    """
    Get data hashes from a step by converting each table cell to the
    appropriate data type.

    If the object is already a list of hashes, it is returned unchanged.
    """

    if hasattr(data, 'hashes'):
        return list(map(hash_data, data.hashes))
    else:
        return data


def get_model(model):
    """
    Convert a model's verbose name to the model class. This allows us to
    use the models verbose name in steps.
    """

    name = model.lower()
    model = MODELS.get(model, None)

    assert model, "Could not locate model by name '%s'" % name

    return model


def reset_sequence(model):
    """
    Reset the ID sequence for a model.
    """
    sql = connection.ops.sequence_reset_sql(no_style(), [model])
    for cmd in sql:
        connection.cursor().execute(cmd)


def create_models(model, data):
    """
    Create models for each data hash. Wrapper around write_models.
    """
    return write_models(model, data, None)


def write_models(model, data, field=None):
    """
    Create or update models for each data hash. If field is present, it is the
    field that is used to get the existing models out of the database to update
    them; otherwise, new models are created.
    """
    data = hashes_data(data)

    written = []

    for hash_ in data:
        if field:
            if field not in hash_:
                raise KeyError(("The \"%s\" field is required for all update "
                                "operations") % field)

            model_kwargs = {field: hash_[field]}
            model_obj = model.objects.get(**model_kwargs)

            for to_set, val in hash_.items():
                setattr(model_obj, to_set, val)

            model_obj.save()

        else:
            model_obj = model.objects.create(**hash_)

        written.append(model_obj)

    reset_sequence(model)
    return written


def _dump_model(model, attrs=None):
    """
    Dump the model fields for debugging.
    """

    fields = []

    for field in model._meta.fields:
        fields.append((field.name, str(getattr(model, field.name))))

    if attrs is not None:
        for attr in attrs:
            fields.append((attr, str(getattr(model, attr))))

    for field in model._meta.many_to_many:
        vals = getattr(model, field.name)
        fields.append(field.name, '{val} ({count})'.format(
            val=', '.join(map(str, vals.all())),
            count=vals.count(),
        ))

    print(', '.join(
        '{0}={1}'.format(field, value)
        for field, value in fields
    ))


def test_existence(model_or_queryset, data):
    """
    Test existence of a given hash in a queryset (or among all model instances
    if a model is given).
    """

    try:
        queryset = model_or_queryset.objects
    except AttributeError:
        queryset = model_or_queryset

    fields = {}
    extra_attrs = {}
    for k, v in data.items():
        if k.startswith('@'):
            # this is an attribute
            extra_attrs[k[1:]] = v
        else:
            fields[k] = v

    filtered = queryset.filter(**fields)

    if filtered.exists():
        return any(
            all(getattr(obj, k) == v for k, v in extra_attrs.items())
            for obj in filtered.all()
        )

    return False


def models_exist(model, data, queryset=None,
                 existence_check=None,
                 should_exist=True):
    """
    Check whether the models defined by @data exist in the @queryset.
    """

    data = hashes_data(data)

    if not queryset:
        queryset = model.objects

    failed = 0
    try:
        for hash_ in data:
            if existence_check:
                match = existence_check(hash_)
            else:
                match = test_existence(queryset, hash_)

            if should_exist:
                assert match, \
                    "%s does not exist: %s" % (model.__name__, hash_)
            else:
                assert not match, \
                    "%s exists: %s" % (model.__name__, hash_)

    except AssertionError as exc:
        print(exc)
        failed += 1

    if failed:
        print("Rows in DB are:")
        for model in queryset.all():
            _dump_model(model,
                        attrs=[k[1:]
                               for k in data[0].keys()
                               if k.startswith('@')])

        if should_exist:
            raise AssertionError("%i rows missing" % failed)
        else:
            raise AssertionError("%i rows found" % failed)


def write_models_generic(data, model, field=None):
    """
    And I have foos in the database:
        | name | bar  |
        | Baz  | Quux |

    And I update existing foos by pk in the database:
        | pk | name |
        | 1  | Bar  |

    The generic method can be overridden for a specific model by defining a
    function write_badgers(data, field), which creates and updates
    the Badger model and decorating it with the writes_models(model_class)
    decorator.

    @writes_models(Profile)
    def write_profile(data, field):
        '''Creates a Profile model'''

        for hash_ in data:
            if field:
                profile = Profile.objects.get(**{field: hash_[field]})
                else:
                    profile = Profile()

                ...
    """

    data = hashes_data(data)

    model = get_model(model)

    try:
        func = _WRITE_MODEL[model]
    except KeyError:
        func = curry(write_models, model)
    func(data, field)


for txt in (
    (r'I have(?: an?)? ([a-z][a-z0-9_ ]*) in the database:'),
    (r'I update(?: an?)? existing ([a-z][a-z0-9_ ]*) by ([a-z][a-z0-9_]*) '
     'in the database:'),
):
    step(txt)(write_models_generic)


@step(STEP_PREFIX + r'([A-Z][a-z0-9_ ]*) with ([a-z]+) "([^"]*)"' +
      r' has(?: an?)? ([A-Z][a-z0-9_ ]*) in the database:')
def create_models_for_relation(step, rel_model_name,
                               rel_key, rel_value, model):
    """
    And project with name "Ball Project" has goals in the database:
    | description                             |
    | To have fun playing with balls of twine |
    """

    lookup = {rel_key: rel_value}
    rel_model = get_model(rel_model_name).objects.get(**lookup)

    data = hashes_data(step)

    for hash_ in data:
        hash_['%s' % rel_model_name] = rel_model

    write_models_generic(data, model)


@step(STEP_PREFIX + r'([A-Z][a-z0-9_ ]*) with ([a-z]+) "([^"]*)"' +
      r' is linked to ([A-Z][a-z0-9_ ]*) in the database:')
def create_m2m_links(step, rel_model_name, rel_key, rel_value, relation_name):
    """
    And article with name "Guidelines" is linked to tags in the database:
    | name   |
    | coding |
    | style  |
    """

    lookup = {rel_key: rel_value}
    rel_model = get_model(rel_model_name).objects.get(**lookup)
    relation = None
    for m2m in rel_model._meta.many_to_many:
        if relation_name in (m2m.name, m2m.verbose_name):
            relation = getattr(rel_model, m2m.name)
            break
    if not relation:
        try:
            relation = getattr(rel_model, relation_name)
        except AttributeError:
            pass
    assert relation, \
        "%s does not have a many-to-many relation named '%s'" % (
            rel_model._meta.verbose_name.capitalize(),
            relation_name,
        )
    m2m_model = relation.model

    for hash_ in step.hashes:
        relation.add(m2m_model.objects.get(**hash_))


@step(STEP_PREFIX + r'(?:an? )?([A-Z][a-z0-9_ ]*) should be present ' +
      r'in the database')
def models_exist_generic(step, model):
    """
    And objectives should be present in the database:
    | description      |
    | Make a mess      |
    """

    return models_existence_generic(step, model, True)


@step(STEP_PREFIX + r'(?:an? )?([A-Z][a-z0-9_ ]*) should not be present ' +
      r'in the database')
def models_exist_generic(step, model):
    """
    And objectives should not be present in the database:
    | description      |
    | Make a mess      |
    """

    return models_existence_generic(step, model, False)


def models_existence_generic(step, model, should_exist):
    """
    Assert the models are present or absent in the database.
    """

    model = get_model(model)

    try:
        func = _MODEL_EXISTS[model]
    except KeyError:
        func = curry(models_exist, model)

        try:
            existence_check = _TEST_MODEL[model]
            func = partial(func, existence_check=existence_check)
        except KeyError:
            pass

        func = partial(func, should_exist=should_exist)

    func(step)


@step(r'There should be (\d+) ([a-z][a-z0-9_ ]*) in the database')
def model_count(step, count, model):
    """
    Then there should be 0 goals in the database
    """

    model = get_model(model)

    expected = int(count)
    found = model.objects.count()
    assert found == expected, "Expected %d %s, found %d." % \
        (expected, model._meta.verbose_name_plural, found)
