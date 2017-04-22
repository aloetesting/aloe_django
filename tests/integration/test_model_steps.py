# -*- coding: utf-8 -*-
"""
Test model update steps.
"""

from __future__ import unicode_literals

import unittest

import django

from aloe.utils import PY2

from tests.util import in_directory, run_scenario


class ModelStepsTest(unittest.TestCase):
    """Test model update steps."""

    @in_directory(__file__, 'django', 'dill')
    def test_model_creation(self):
        'Models are created through Lettuce steps'

        status, out = run_scenario('leaves', 'create')
        self.assertEqual(status, 0, out)

    @in_directory(__file__, 'django', 'dill')
    def test_model_update(self):
        'Models are updated through Lettuce steps'

        status, out = run_scenario('leaves', 'update', 1)
        self.assertEqual(status, 0, out)

        status, out = run_scenario('leaves', 'update', 2)
        self.assertNotEqual(status, 0, out)
        self.assertIn("IntegrityError", out)

        status, out = run_scenario('leaves', 'update', 3)
        self.assertNotEqual(status, 0, out)
        self.assertIn(
            "The \"pk\" field is required for all update operations", out)

        status, out = run_scenario('leaves', 'update', 4)
        self.assertEqual(status, 0, out)

    @in_directory(__file__, 'django', 'dill')
    def test_model_existence_check(self):
        'Model existence is checked through Lettuce steps'

        status, out = run_scenario('leaves', 'existence', 1)
        self.assertEqual(status, 0, out)

        # One of the gardens has a non-ASCII name. On Python 2 under
        # Django >= 1.9, it gets output by Nose using the escapes.
        grdn4 = '颐和园'
        if PY2 and django.VERSION >= (1, 9):
            grdn4 = grdn4.encode('unicode_escape')

        status, out = run_scenario('leaves', 'existence', 2)
        self.assertNotEqual(status, 0)
        self.assertIn(
            "Garden does not exist: {0}".format(
                {'name': 'Botanic Gardens'}
            ),
            out
        )
        gardens = "\n".join([
            "Rows in DB are:",
            "id=1, name=Secret Garden, area=45, raining=False",
            "id=2, name=Octopus's Garden, area=120, raining=True",
            "id=3, name=Covent Garden, area=200, raining=True",
            "id=4, name={}, area=500, raining=False".format(grdn4),
        ])

        self.assertIn(gardens, out)
        self.assertIn("AssertionError: 1 rows missing", out)

        status, out = run_scenario('leaves', 'existence', 3)
        self.assertNotEqual(status, 0)
        # Cannot check exact string because the order isn't stable
        self.assertIn("Garden does not exist: ", out)
        self.assertIn(str({'name': 'Secret Garden'})[1:-1], out)
        self.assertIn(str({'@howbig': 'huge'})[1:-1], out)
        gardens = "\n".join([
            "Rows in DB are:",
            "id=1, name=Secret Garden, area=45, raining=False, howbig=small",
            (
                "id=2, name=Octopus's Garden, area=120, "
                "raining=True, howbig=medium"
            ),
            "id=3, name=Covent Garden, area=200, raining=True, howbig=big",
            "id=4, name={}, area=500, raining=False, howbig=big".format(grdn4),
        ])
        self.assertIn(gardens, out)
        self.assertIn("AssertionError: 1 rows missing", out)

        status, out = run_scenario('leaves', 'existence', 4)
        self.assertNotEqual(status, 0)
        self.assertIn("Expected 2 geese, found 1", out)

        status, out = run_scenario('leaves', 'existence', 5)
        self.assertNotEqual(status, 0)
        # Cannot check exact string because the order isn't stable
        self.assertIn("Garden exists: ", out)
        self.assertIn(str({'name': 'Secret Garden'})[1:-1], out)
        self.assertIn(str({'@howbig': 'small'})[1:-1], out)
        self.assertIn("AssertionError: 1 rows found", out)
        gardens = "\n".join([
            "Rows in DB are:",
            "id=1, name=Secret Garden, area=45, raining=False, howbig=small",
            (
                "id=2, name=Octopus's Garden, area=120, "
                "raining=True, howbig=medium"
            ),
            "id=3, name=Covent Garden, area=200, raining=True, howbig=big",
            "id=4, name={}, area=500, raining=False, howbig=big".format(grdn4),
        ])
        self.assertIn(gardens, out)
