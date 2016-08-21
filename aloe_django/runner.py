"""
Test runner running the Gherkin tests.
"""

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
