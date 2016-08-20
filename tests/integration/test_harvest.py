# -*- coding: utf-8 -*-
"""
Test the harvest command.
"""

import unittest

from tests.util import in_directory, run_scenario


class HarvestTest(unittest.TestCase):
    """Test the harvest command."""

    @in_directory(__file__, 'django', 'alfaces')
    def test_django_agains_alfaces(self):
        """running the "harvest" django command with verbosity 3"""

        status, out = run_scenario()
        self.assertEqual(status, 0, out)

        self.assertIn("Test the django app DO NOTHING", out)
        self.assertIn("Test the django app FOO BAR", out)

    @in_directory(__file__, 'django', 'alfaces')
    def test_running_only_specified_features(self):
        """it can run only the specified features, passing the file path"""

        status, out = run_scenario('foobar', 'foobar')

        self.assertEqual(status, 0, out)

        self.assertIn("Test the django app FOO BAR", out)
        self.assertNotIn("Test the django app DO NOTHING", out)

    @in_directory(__file__, 'django', 'alfaces')
    def test_specifying_features_in_inner_directory(self):
        """it can run only the specified features from a subdirectory"""

        status, out = run_scenario('foobar', 'deeper/deeper/leaf')

        self.assertEqual(status, 0, out)

        self.assertNotIn("Test the django app FOO BAR", out)
        self.assertIn("Test a feature in an inner directory", out)
        self.assertNotIn("Test the django app DO NOTHING", out)

    @in_directory(__file__, 'django', 'kale')
    def test_run_with_tags(self):
        """it will only run specified tags"""

        status, out = run_scenario(attr='!fails')

        self.assertEqual(status, 0, out)
        self.assertIn("Ran 2 tests", out)

    @in_directory(__file__, 'django', 'kale')
    def test_run_with_tags_and_features(self):
        """it will only run specified tags in the feature files"""

        status, out = run_scenario('donothing', attr='!passes,!fails')

        self.assertEqual(status, 0, out)
        self.assertIn("Ran 1 test", out)
