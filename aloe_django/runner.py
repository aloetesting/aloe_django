"""
Test runner running the Gherkin tests.
"""

import os

from django.core.exceptions import ImproperlyConfigured
from django.test.runner import DiscoverRunner

from aloe.loader import GherkinLoader
from aloe.main import AloeOptions
from aloe.result import AloeTestResult
from aloe.runner import GherkinRunner

from aloe_django import TestCase


class GherkinTestRunner(AloeOptions, DiscoverRunner):
    """
    A Django test runner using the Gherkin test runner and loader.
    (note: Django test runner is a different interface to unittest's test
    runner.)
    """

    test_class = TestCase
    test_runner = GherkinRunner

    @classmethod
    def add_arguments(cls, parser):
        """Add the Aloe options to the Django argument parser."""

        return cls.add_aloe_options(parser)

    def __init__(self, *args, **kwargs):
        """Set up the test loader."""

        super(GherkinTestRunner, self).__init__(*args, **kwargs)
        self.test_loader = GherkinLoader()
        self.configure_loader(self.test_loader)

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        """
        Add Gherkin features given as parameters to the test list.

        Django test runner doesn't support specifying path/to/gherkin.feature
        (or even path/to/module.py), so get those out of test_labels and add to
        extra_tests.
        """

        extra_tests = extra_tests or []

        new_test_labels = []
        for label in test_labels:
            if os.path.isfile(label) and label.endswith('.feature'):
                extra_tests += self.test_loader.loadTestsFromName(label)
                # Leaving the feature file name in test_labels will lead to
                # Django test runner failing: for found paths, instead of
                # loadTestsFromName, discover() is called but doesn't discover
                # anything.
                #
                # Removing the feature file name means if _only_ the feature
                # files are given, test_labels will be empty, leading to
                # running discovery on the current directory (in addition to
                # Gherkin tests already provided).
                #
                # Thus, the only option is to insert a fake label so no tests
                # are discovered from it.
                new_test_labels.append('__fakelabel__')
            else:
                new_test_labels.append(label)

        return super(GherkinTestRunner, self).build_suite(
            new_test_labels,
            extra_tests,
            **kwargs
        )

    def test_runner(self, *args, **kwargs):
        """Pass extra arguments to the test runner."""
        kwargs.update(self.extra_runner_args())
        return GherkinRunner(*args, **kwargs)

    def get_resultclass(self):
        """
        Don't explicitly pass the result class; use the test runner default
        result.
        """

        resultclass = super(GherkinTestRunner, self).get_resultclass()
        if resultclass is not None:
            raise ImproperlyConfigured(
                "Aloe-Django doesn't support custom test result classes."
            )
        return None
